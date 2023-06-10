import requests
from django.http import JsonResponse


def get_response_time(request):
    dominio = request.GET.get("dominio", "")
    ip = request.GET.get("ip", "")

    if not dominio:
        return JsonResponse(
            {"error": "El parámetro 'dominio' es obligatorio"},
            status=400,
        )

    url = f'http://{ip or dominio}'

    try:
        headers = {}
        status_code = ''

        # If an IP is provided, in order to avoid SSL errors or status>400,
        # a "Host" with value="dominio" is added to the Header.
        if ip:
            headers['Host'] = dominio

        # allow_redirects=False prevents redirects in order to correctly
        # calculate the response time to the first URL.
        response = requests.get(
            url,
            headers=headers,
            allow_redirects=False,
            timeout=10
        )
        status_code = response.status_code
        response.raise_for_status()

        response_time = (response.elapsed.total_seconds() * 1000)

        return JsonResponse(
            {
                'status': status_code,
                'time': f'{response_time:.0f}ms',
            },
            status=status_code
        )

    except requests.RequestException as e:
        return JsonResponse(
            {'error': f'{e}'},
            status=(status_code if status_code else 500),
        )
