from django.core.paginator import Paginator
from django.http import JsonResponse


def paginate(request, object_list, items_per_page=12):
    paginator = Paginator(object_list, items_per_page)
    return paginator.get_page(request.GET.get("page"))


def json_error(message, status):
    return JsonResponse({"error": message}, status=status)
