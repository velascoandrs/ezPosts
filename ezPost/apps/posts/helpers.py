from django.shortcuts import redirect


def handle_uploaded_file(f):
    with open('media/post/portadas/{}'.format(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

