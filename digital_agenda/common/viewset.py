from django.utils.encoding import escape_uri_path
from rest_framework.response import Response


class FilenameExportMixin:
    filename = "export.csv"

    def get_filename(self, request, *args, **kwargs):
        return self.filename

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        filename = escape_uri_path(self.get_filename(request, *args, **kwargs))
        if (
            isinstance(response, Response)
            and response.accepted_renderer.format == "csv"
        ):
            response["content-disposition"] = f"attachment; filename={filename}"
        return response
