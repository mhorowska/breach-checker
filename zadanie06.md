1. 
```
PS C:\Users\box\metody_lab\breach-checker> docker compose exec backend pytest -v
================ test session starts ================
platform linux -- Python 3.12.16, pytest-8.4.2, pluggy-1.7.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
rootdir: /app
collected 8 items                                   

tests/test_check.py::test_leaked_hash_is_found PASSED [ 12%]
tests/test_check.py::test_unknown_hash_is_not_found PASSED [ 25%]
tests/test_check.py::test_missing_hash_field PASSED [ 37%]
tests/test_check.py::test_plaintext_password_is_rejected PASSED [ 50%]
tests/test_check.py::test_uppercase_leaked_hash_is_found PASSED [ 62%]
tests/test_check.py::test_short_hash_39_chars_is_rejected PASSED [ 75%]
tests/test_check.py::test_non_hex_hash_is_rejected PASSED [ 87%]
tests/test_check.py::test_non_json_body_is_rejected PASSED [100%]

================= 8 passed in 0.34s =================


PS C:\Users\box\metody_lab\breach-checker> docker compose exec backend pytest
============================================================ test session starts =============================================================
platform linux -- Python 3.12.16, pytest-8.4.2, pluggy-1.7.0
rootdir: /app
collected 8 items                                                                                                                            

tests/test_check.py ....F...                                                                                                           [100%]

================================================================== FAILURES ==================================================================
____________________________________________________ test_uppercase_leaked_hash_is_found _____________________________________________________

client = <FlaskClient <Flask 'app'>>

    def test_uppercase_leaked_hash_is_found(client):
        response = client.post("/check", json={"hash": LEAKED.upper()})
>       assert response.status_code == 200
E       assert 400 == 200
E        +  where 400 = <WrapperTestResponse streamed [400 BAD REQUEST]>.status_code

tests/test_check.py:26: AssertionError
========================================================== short test summary info ===========================================================
FAILED tests/test_check.py::test_uppercase_leaked_hash_is_found - assert 400 == 200
======================================================== 1 failed, 7 passed in 0.45s =========================================================

What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error"
```
Testy z zajęć nie wykryły usunięcia .lower(), ponieważ wszystkie testowane skróty (LEAKED i NOT_LEAKED) były zapisane wyłącznie małymi literami. Dopiero test wysyłający skrót wielkimi literami (LEAKED.upper()) sprawdził normalizację wielkości znaków przed walidacją i zapytaniem do bazy.

2. 
HTTP 500
```
NAME                        IMAGE                                                                     COMMAND                  SERVICE    CREATED        STATUS                      PORTS
breach-checker-backend-1    breach-checker-backend                                                    "flask --app app run…"   backend    13 hours ago   Exited (1) 33 seconds ago   
breach-checker-db-1         postgres:16-alpine                                                        "docker-entrypoint.s…"   db         13 hours ago   Exited (0) 2 minutes ago    
breach-checker-frontend-1   sha256:e5be4d9b2a81475269bea420783151f1ae30583bcbeb8090c9b649bb1460d789   "/docker-entrypoint.…"   frontend   7 days ago     Up 7 days                   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

PS C:\Users\box\metody_lab\breach-checker> docker inspect --format '{{.State.Status}} {{.State.ExitCode}}' breach-checker-backend-1
exited 1
```

### Porównanie awarii z blokadą

| Cecha | Awaria (wyłączona baza + restart) | 
| :--- | :--- | :--- |
Blokada (`LOCK TABLE` z kroku 4) |
| **Status w `docker compose ps`** | `Exited (1)` | `Up (healthy)` |
| **CPU w `docker stats`** | Brak (kontener zatrzymany) | ~0% |
| **Ostatnie linie logów** | Ślad stosu (traceback) i błąd połączenia z bazą (`psycopg2.OperationalError`) | `check: hash=...`, brak linii `POST /check 200` |
| **Co dostał klient** | `HTTP 500` ze stroną debuggera (`blad.html`); po restarcie `502 Bad Gateway` | `504 Gateway Time-out` („Brak połączenia z backendem”) |
| **Po jakim czasie** | Natychmiast (ułamek sekundy) | Po 60 sekundach (timeout nginx) |

Plik blad.html zawierał stronę interaktywnego debuggera Flaska (Werkzeug) z pełnym śladem stosu (tracebackiem), fragmentami kodu źródłowego oraz szczegółami błędu połączenia z bazą. Na serwerze produkcyjnym byłoby to poważne zagrożenie bezpieczeństwa, ponieważ ujawnia atakującemu wewnętrzną strukturę aplikacji i ścieżki plików, a sam debugger umożliwia zdalne wykonywanie kodu Pythona na serwerze (chronione jedynie kodem PIN).

3.
StatusCode        : 200
StatusDescription : OK
Content           : {115, 101, 114, 118...}
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Accept-Ranges: bytes
                    Content-Length: 191
                    Content-Type: application/octet-stream
                    Date: Fri, 27 Nov 2026 10:12:08 GMT
                    ETag: "6b00010f-bf"
                    Last-Modified: Fri...
Headers           : {[Connection, keep-alive], [Accept-Ranges, bytes], [Content-Length, 191], [Content-Type, application/octet-stream]...}
RawContentLength  : 191

PS C:\Users\box\metody_lab\breach-checker> curl.exe -I http://localhost:8080/nginx.conf
HTTP/1.1 404 Not Found
Server: nginx/1.31.8
Date: Fri, 27 Nov 2026 10:14:23 GMT
Content-Type: text/html
Content-Length: 153
Connection: keep-alive

Obraz produkcyjny frontendu nie ma tego problemu, ponieważ frontend/Dockerfile kopiuje do /usr/share/nginx/html wyłącznie wybrane pliki strony (index.html, style.css, script.js), bez nginx.conf i Dockerfile. Montowanie całego katalogu projektu do katalogu publicznego serwera WWW jest ryzykowne, ponieważ udostępnia w sieci pliki konfiguracyjne, definicje obrazów lub inne wrażliwe pliki, które nigdy nie powinny być dostępne dla użytkowników.