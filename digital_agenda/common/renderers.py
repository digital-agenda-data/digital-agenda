from rest_framework_csv.renderers import CSVRenderer


class CustomCSVRenderer(CSVRenderer):
    def flatten_list(self, obj):
        # Normally, a list would be split into multiple keys with the index appended.
        # Instead of that, just convert to a comma-separated list.
        return {"": ",".join(map(str, obj))}
