1.
PS C:\Users\box\OneDrive\Desktop\breach-checker> docker history mhorowska-frontend:v1
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
8a01e755200b   22 minutes ago   EXPOSE [80/tcp]                                 0B        buildkit.dockerfile.v0
<missing>      22 minutes ago   RUN /bin/sh -c htmlhint /usr/share/nginx/htm…   4.1kB     buildkit.dockerfile.v0
<missing>      22 minutes ago   COPY . /usr/share/nginx/html # buildkit         32.8kB    buildkit.dockerfile.v0
<missing>      22 minutes ago   RUN /bin/sh -c apk add --no-cache nodejs npm…   99.3MB    buildkit.dockerfile.v0
<missing>      22 minutes ago   LABEL autor=mhorowska data=2026-10-14           0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      RUN /bin/sh -c set -x     && apkArch="$(cat …   52.4MB    buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV ACME_VERSION=0.4.1                          0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV NJS_RELEASE=1                               0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV NJS_VERSION=1.0.2                           0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      CMD ["nginx" "-g" "daemon off;"]                0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      STOPSIGNAL SIGQUIT                              0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      EXPOSE map[80/tcp:{}]                           0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ENTRYPOINT ["/docker-entrypoint.sh"]            0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      COPY 30-tune-worker-processes.sh /docker-ent…   16.4kB    buildkit.dockerfile.v0
<missing>      2 weeks ago      COPY 20-envsubst-on-templates.sh /docker-ent…   12.3kB    buildkit.dockerfile.v0
<missing>      2 weeks ago      COPY 15-local-resolvers.envsh /docker-entryp…   12.3kB    buildkit.dockerfile.v0
<missing>      2 weeks ago      COPY 10-listen-on-ipv6-by-default.sh /docker…   12.3kB    buildkit.dockerfile.v0
<missing>      2 weeks ago      COPY docker-entrypoint.sh / # buildkit          8.19kB    buildkit.dockerfile.v0
<missing>      2 weeks ago      RUN /bin/sh -c set -x     && addgroup -g 101…   5.75MB    buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV DYNPKG_RELEASE=1                            0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV PKG_RELEASE=1                               0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV NGINX_VERSION=1.31.8                        0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      LABEL maintainer=NGINX Docker Maintainers <d…   0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ADD alpine-minirootfs-3.24.3-x86_64.tar.gz /…   9.08MB    buildkit.dockerfile.v0
PS C:\Users\box\OneDrive\Desktop\breach-checker> 

PS C:\Users\box\OneDrive\Desktop\breach-checker> docker inspect --format '{{json .Config.Labels}}' mhorowska-frontend:v1      
{"autor":"mhorowska","data":"2026-10-14","maintainer":"NGINX Docker Maintainers <docker-maint@nginx.com>"}

Warstwy nowsze pochodzą z mojego pliku Dockerfile, natomiast warstwy starsze zostały odziedziczone z obrazu bazowego nginx:alpine. Rozmiar 0B posiadają instrukcje takie jak LABEL, EXPOSE, ENV, CMD czy ENTRYPOINT, ponieważ dopisują one do obrazu wyłącznie metadane i nie powiększają systemu plików.

2
Fri Nov  6 09:58:38 UTC 2026
Fri Nov  6 09:58:38 UTC 2026

PS C:\Users\box\OneDrive\Desktop\breach-checker> docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS              PORTS                                     NAMES
03a1d1023e1e   mhorowska-frontend:v2   "/docker-entrypoint.…"   50 seconds ago       Up 49 seconds       0.0.0.0:8082->80/tcp, [::]:8082->80/tcp   frontend2
b8c94af3c492   mhorowska-frontend:v2   "/docker-entrypoint.…"   About a minute ago   Up About a minute   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp   frontend1

Instrukcja RUN wykonuje się tylko raz w trakcie budowania obrazu (docker build), a jej wynik jest na stałe zapisywany w warstwie obrazu. Uruchamiane kontenery współdzielą ten sam wygenerowany wcześniej plik, ponieważ instrukcje RUN nie wykonują się przy ich starcie

3
    root   /usr/share/nginx/html;

4

PS C:\Users\box\OneDrive\Desktop\breach-checker> docker exec frontend_bad_copy ls /usr/share/nginx
html
index.html
script.js
style.css
 S C:\Users\box\OneDrive\Desktop\breach-checker> docker exec frontend_bad_copy ls /usr/share/nginx/html
50x.html
build.txt
index.html
PS C:\Users\box\OneDrive\Desktop\breach-checker> 

Narzędzie htmlhint sprawdziło domyślny plik index.html serwera Nginx, który znajdował się w katalogu /usr/share/nginx/html/. Budowanie przeszło bez błędu, ponieważ ten domyślny plik Nginx jest poprawnym dokumentem HTML i nie zawiera błędów składniowych, a nasze pliki z błędem trafiły do innego katalogu (/usr/share/nginx/)
