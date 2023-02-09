from django.utils.encoding import escape_uri_path
from rest_framework.response import Response



class FilenameExportMixin:
    filename = "download"

    def get_filename(self, request, *args, **kwargs):
        return self.filename

    def finalize_response(self, request, response, *args, **kwargs):
        formats = ("csv", "xlsx")
        response = super().finalize_response(request, response, *args, **kwargs)
        if (
            isinstance(response, Response)
            and response.accepted_renderer.format in formats
        ):
            filename = (
                escape_uri_path(self.get_filename(request, *args, **kwargs))
                + "."
                + response.accepted_renderer.format
            )
            response["content-disposition"] = f"attachment; filename={filename}"
        return response

