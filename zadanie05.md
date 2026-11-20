1.
 docker compose up -d --build
✔ Image breach-checker-backend        Built                3.1s
 ✔ Image breach-checker-frontend       Built                3.1s
 ✔ Network breach-checker_default      Created              0.0s
 ✔ Container breach-checker-db-1       Healthy              6.1s
 ✔ Container breach-checker-backend-1  Healthy             11.8s
 ✔ Container breach-checker-frontend-1 Started             12.0s

docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED          STATUS                    PORTS
breach-checker-backend-1    breach-checker-backend    "python app.py"          backend    43 seconds ago   Up 36 seconds (healthy)   5000/tcp
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         43 seconds ago   Up 42 seconds (healthy)   5432/tcp
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   43 seconds ago   Up 31 seconds             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

2.
'{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d "@-"

sprawdzenie skrótu przez API:
    {"found":true}

przez zatrzymanie bez usuwania wolumenów:
    {"found":true}

przez zatrzymanie z usunięciem wolumenów:
    {"found":false}

Po usunieciu kontenerów nadal zostaje wolumen w którym PostgreSQL przechowuje dane. Jak usuniemy też wolumen to cala zawartosc bazy znika. Po down -v w bazie znów są 89 skróty z próbki poniewaz postgres automatycznie wykonał skrypt init.sql 

3.
PS C:\Users\box\metody_lab\breach-checker> docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED          STATUS                    PORTS
breach-checker-backend-1    breach-checker-backend    "python app.py"          backend    13 minutes ago   Up 13 minutes (healthy)   5000/tcp
breach-checker-backend-2    breach-checker-backend    "python app.py"          backend    9 seconds ago    Up 8 seconds (healthy)    5000/tcp
breach-checker-backend-3    breach-checker-backend    "python app.py"          backend    9 seconds ago    Up 8 seconds (healthy)    5000/tcp
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         13 minutes ago   Up 13 minutes (healthy)   5432/tcp
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   13 minutes ago   Up 13 minutes             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
PS C:\Users\box\metody_lab\breach-checker> docker compose exec frontend nslookup backend
Server:         127.0.0.11
Address:        127.0.0.11:53

Non-authoritative answer:

Non-authoritative answer:
Name:   backend
Address: 172.19.0.5
Name:   backend
Address: 172.19.0.6
Name:   backend
Address: 172.19.0.3

PS C:\Users\box\metody_lab\breach-checker> docker compose logs --tail=40 backend | Select-String "POST /check"                                                                
                                                              
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:44:43] "POST /check HTTP/1.1" 200 -
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:44:43] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:44:43] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:44:43] "POST /check HTTP/1.1" 200 -
backend-1  | 172.19.0.4 - - [20/Nov/2026 09:44:43] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:15] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -
backend-3  | 172.19.0.4 - - [20/Nov/2026 09:47:16] "POST /check HTTP/1.1" 200 -

Przed restartem frontendu wszystkie zapytania trafiały do jednej kopii, ponieważ nginx sprawdza adresy IP przypisane do nazwy backend tylko raz kiedy sie uruchamia, kiedy działała jeszcze tylko jedna replika. Dopiero po restarcie pobrał z DNS aktualną listę wszystkich trzech kopii.