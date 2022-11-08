import contentDisposition from "content-disposition";
import mimeTypes from "@/lib/mimeTypes";

const apiBaseEndpoint = "/api/v1";

export let apiHost = window.location.host;
export let apiURL = `${window.location.origin}${apiBaseEndpoint}`;
export let apiBase = `${window.location.origin}`;

if (import.meta.env.DEV) {
  apiHost = "localhost:8000";
  apiURL = `http://localhost:8000${apiBaseEndpoint}`;
  apiBase = "http://localhost:8000";
}

if (import.meta.env.VITE_APP_API_HOST) {
  apiHost = import.meta.env.VITE_APP_API_HOST;
  apiURL = `${window.location.protocol}//${apiHost}${apiBaseEndpoint}`;
  apiBase = `${window.location.protocol}//${apiHost}`;
}

class APIError extends Error {
  constructor(message, details) {
    message = `${message}: ${details.detail}`;
    super(message);
    Object.assign(this, details);
    this.name = "APIError";
  }
}

const getCookie = (name) => {
  const cookie = {};
  document.cookie.split(";").forEach((el) => {
    const [k, v] = el.split("=");
    cookie[k.trim()] = v;
  });
  return cookie[name];
};

export function downloadFile(blob, filename) {
  if (typeof window.navigator.msSaveBlob !== "undefined") {
    // IE workaround for "HTML7007: One or more blob URLs were
    // revoked by closing the blob for which they were created.
    // These URLs will no longer resolve as the data backing
    // the URL has been freed."
    window.navigator.msSaveBlob(blob, filename);
  } else {
    const blobURL = window.URL.createObjectURL(blob);
    const tempLink = document.createElement("a");
    tempLink.style.display = "none";
    tempLink.href = blobURL;
    tempLink.setAttribute("download", filename);

    // Safari thinks _blank anchor are pop ups. We only want to set _blank
    // target if the browser does not support the HTML5 download attribute.
    // This allows you to download files in desktop safari if pop up blocking
    // is enabled.
    if (typeof tempLink.download === "undefined") {
      tempLink.setAttribute("target", "_blank");
    }

    document.body.appendChild(tempLink);
    tempLink.click();
    document.body.removeChild(tempLink);
    window.URL.revokeObjectURL(blobURL);
  }
}

/**
 * Calls the apiCall function, but enables the browser cache.
 *
 * @return {Promise<Object>}
 */
export async function cachedApiCall(
  method = "GET",
  endpoint = "/",
  params = {},
  data = undefined,
  contentType = "application/json"
) {
  return apiCall(method, endpoint, params, data, contentType, "default");
}

/**
 * Calls the apiCall function, but downloads the response instead of returning it.
 *
 * @return {Promise<Object>}
 */
export async function downloadApiCall(
  method = "GET",
  endpoint = "/",
  params = {},
  data = undefined,
  contentType = "application/json"
) {
  return apiCall(method, endpoint, params, data, contentType, "no-cache", true);
}

/**
 * Resolve a promise and ignored all API errors or only the specified ones.
 *
 * @param promise {Promise}
 * @param returnValue {*} what should be returned instead of the error
 * @param ignoredErrors {Array} list of error codes to ignore, if not given
 *  all errors are ignored instead
 * @return {Promise<null|*>}
 */
export async function ignoreAPIError(
  promise,
  returnValue = null,
  ignoredErrors = null
) {
  try {
    return await promise;
  } catch (e) {
    if (!ignoredErrors || ignoredErrors.indexOf(e.statusCode) !== -1) {
      return returnValue;
    }
    throw e;
  }
}

/**
 * Perform an API call to the backend.
 *
 * @param method {string} HTTP method to use
 * @param endpoint {string} API endpoint or full URL.
 * @param params {Object|Array} Object with URL parameters. Alternatively an Array can
 *  be passed as parameters with pairs of (key, value). This can be used
 *  when repeating query args needs to be passed to the API.
 * @param {Object} data request body
 * @param contentType {string} specify the request body content type
 * @param cacheMode {string} value for Request.cache
 * @param download
 * @returns {Promise<Object>} rejects in case of connection or HTTP Errors.
 */
export async function apiCall(
  method = "GET",
  endpoint = "/",
  params = {},
  data = undefined,
  contentType = "application/json",
  cacheMode = "no-cache",
  download = false
) {
  let url;
  if (!endpoint) return;

  if (endpoint.startsWith(apiURL)) {
    url = new URL(endpoint);
  } else {
    url = new URL(apiURL + endpoint);
  }

  if (!Array.isArray(params)) {
    params = Object.entries(params);
  }
  params.forEach((entry) => {
    url.searchParams.append(entry[0], entry[1]);
  });

  const csrfToken = getCookie("csrftoken");
  const fetchOptions = {
    method,
    mode: "cors",
    cache: cacheMode,
    credentials: "include",
    headers: {
      Accept: "application/json",
    },
    redirect: "follow",
  };
  if (data) {
    switch (contentType) {
      case "multipart/form-data":
        fetchOptions.body = new FormData();
        Object.entries(data).forEach((value) => {
          fetchOptions.body.append(...value);
        });
        break;
      case "application/json":
        fetchOptions.headers["Content-Type"] = contentType;
        fetchOptions.body = JSON.stringify(data);
        break;
      default:
        fetchOptions.headers["Content-Type"] = contentType;
        fetchOptions.body = data;
    }
  }
  if (csrfToken) {
    fetchOptions.headers["X-CSRFToken"] = csrfToken;
  }

  return await _apiCall(url, fetchOptions, download);
}

/***
 * Performs the actual api call and does error handling.
 *
 * @param url
 * @param fetchOptions
 * @param download
 * @return {Promise<{}|*>}
 * @private
 */
async function _apiCall(url, fetchOptions, download = false) {
  const response = await fetch(url.toString(), fetchOptions);

  if (!download) {
    return await _processJSONResponse(response);
  }
  return await _processRawResponse(response);
}

async function _processJSONResponse(response) {
  if (response.status === 204) {
    // 204 (No Content)
    return {};
  }

  // We don't know what to do with anything other than a JSON
  // so just quit here and don't read the body.
  if (response.headers.get("Content-Type") !== "application/json") {
    throw new APIError("Unknown API error", {
      requestURL: response.url,
      statusCode: response.status,
      detail: response.statusText,
    });
  }

  let jsonBody;
  jsonBody = await response.json();
  jsonBody.requestURL = new URL(response.url);
  jsonBody.statusCode = response.status;

  if (!response.ok) {
    // We got an expected error from the API, the error handling
    // is passed to the component calling the API.
    throw new APIError("API Error", jsonBody);
  }
  // Success
  return jsonBody;
}

async function _processRawResponse(response) {
  let filename;
  const disposition = response.headers.get("Content-Disposition");
  if (disposition) {
    filename = contentDisposition.parse(disposition).parameters.filename;
  }

  if (!filename) {
    const ext = mimeTypes[response.headers.get("Content-Type")] || "";
    filename =
      response.url
        .split("/")
        .filter((p) => !!p)
        .slice(-1)[0] + ext;
  }

  return downloadFile(await response.blob(), filename);
}

/**
 * Take a media URL and resolve it to an absolute URL.
 *
 * @param mediaURL {string}
 * @returns {string|undefined}
 */
export function apiMediaURL(mediaURL) {
  let url;
  if (!mediaURL) return;
  if (mediaURL.startsWith(apiBase)) {
    url = new URL(mediaURL);
  } else {
    url = new URL(apiBase + mediaURL);
  }
  return url.toString();
}
