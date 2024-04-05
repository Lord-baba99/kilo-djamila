server {
    listen 80;
    server_name kingstinexport.com www.kingstinexport.com;
    
    location /static/ {
        alias /home/ubuntu/site/kilo/static/; # Chemin vers les fichiers statiques montés dans le conteneur
    }

    location / {
        proxy_pass http://localhost:8080; # Remplacez 8000 par le port de votre conteneur
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

sudo docker run -d -p 8888:80 --name nginx -v /home/ubuntu/site/kilo/nginx/conf.d:/etc/nginx/sites-available/ nginx