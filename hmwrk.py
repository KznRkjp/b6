from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:

        result = "Количество найденных альбомов: {}</br>".format(len(albums_list))
        album_names = [album.album for album in albums_list]
        result += "Список альбомов:</br>"
        result += "</br>".join(album_names)
    return result



@route("/albums", method="POST")
def add_album():

    try:
        year = int(request.forms.get("year"))
        artist = str(request.forms.get("artist"))
        genre = str(request.forms.get("genre"))
        album_ = str(request.forms.get("album"))
    except ValueError:

        result = HTTPError(400, "Некорректные параметры")
    else:
        if year>-2000 and year < 2020:
            if not album.in_db(artist, album_):
                album.add(year, artist, genre, album_)
                result = "Альбом {} добавлен".format(album_)
            else:
                result = HTTPError(409, "Запись об альбоме уже имеется.")
        else:
            result = HTTPError(400, "Некорректные параметры (год)")

    return result





if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
