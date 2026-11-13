zad 1
 docker logs backend

172.19.0.1 - - [13/Nov/2026 11:14:47] "GET /health HTTP/1.1" 200 -
172.19.0.1 - - [13/Nov/2026 11:14:55] "GET /health HTTP/1.1" 200 -
172.19.0.1 - - [13/Nov/2026 11:14:56] "GET /health HTTP/1.1" 200 -
172.19.0.1 - - [13/Nov/2026 11:16:14] "GET /health HTTP/1.1" 200 -
{"status":"ok"}

zad 2
PS C:\Users\box\OneDrive\Desktop\breach-checker> docker run --rm --network breach-net healthcheck-probe
backend: OK
docker run --rm healthcheck-probe
backend: UNREACHABLE
docker stop backend
backend
docker run --rm --network breach-net healthcheck-probe
backend: UNREACHABLE


jak nie jest w sieci to nie rozpoznaje po nazwie

zad 3
docker exec backend cat /tmp/notatka.txt
notatka
docker exec backend cat /tmp/notatka.txt
cat: /tmp/notatka.txt: No such file or directory

docker run --rm -v breach-dane:/dane alpine sh -c "date >> /dane/historia.txt && cat /dane/historia.txt"
Fri Nov 13 11:31:51 UTC 2026
Fri Nov 13 11:32:04 UTC 2026
docker volume ls
DRIVER    VOLUME NAME
local     breach-dane
local     projektmetodywirtualizacji_pgdata
docker volume rm breach-dane
breach-dane
poniewaz historia.txt to wolumen niezależny od kontenerów
