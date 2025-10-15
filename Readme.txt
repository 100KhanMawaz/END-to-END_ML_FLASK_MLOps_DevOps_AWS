1st we created our ML model in Jupyter notebook and exported the model as a pickle file

2nd we created backend using flask which uses that model for prediction and providing inputs in the same way how our model is configured in training datasets

3rd we created frontend using ChatGPT. As I don't wanna waste my time in Frontend just make sure your concept is clear so that you can give proper prompts to AI. Here we faced an issue of 400 Bad request because we were not sending the body of the request as expected by our backend so I gave my backend code to ChatGPT He only debugged that issue

4th we are setting up server in Nginx server where we just need to write localhost on our browser and our app will start working basharte Nginx server chalu rehna chaiye.
	
	In this what we did is in drive c > program files > nginx > nginxconf > nginxconf.txt there was sample html welcome page which our Nginx server was rendering so instead of that we will give path to our app.html and it will render that. So how we do this is below:

	  location / {
            root   C:\Users\Moaaz\OneDrive\Desktop\ML\RealState_Project\Client; #path to Nginx server
            index  index.html index.htm app.html; # it will look for either of the three. but it will find only app.html on the above folder instead we could have remove the other 2 but let it be their
        }
	
	Make sure after editing this you END task your NGINX from background processes and restart it

5th we changed the hardcoded url: var url = "http://127.0.0.1:5000/get_location_names" to:     var url = "/api/get_location_names"
 the explanation of chatGPT is as below in nginx.conf:  location /api/{
            rewrite ^/api(.*) $1 break;
            proxy_pass http://127.0.0.1:5000;
        }

EXPLANATION:

location /api/ { ... }

This tells Nginx:
“If a request comes in with a URL starting with /api/, handle it using the rules inside this block.”

Example:

https://mydomain.com/api/get_location_names


rewrite ^/api(.*) $1 break;

This removes the /api prefix from the request path before forwarding it.

^/api(.*) → regex that captures everything after /api

$1 → means “replace with whatever was captured”

break → stop rewriting after this rule

Example:

Incoming: /api/get_location_names
Rewritten: /get_location_names


proxy_pass http://127.0.0.1:5000;

After rewriting, Nginx forwards the request to your Flask app running locally on port 5000.

So effectively:

https://mydomain.com/api/get_location_names
    ⬇️
Nginx rewrites → /get_location_names
    ⬇️
Forwards to http://127.0.0.1:5000/get_location_names

✅ Why it’s used

Frontend ↔ Backend separation: Your frontend may call /api/... endpoints, but Flask doesn’t know about /api — it only has /get_location_names etc.

Nginx acts as a reverse proxy: It strips /api and forwards traffic to Flask.

Security & flexibility: You can later swap Flask for another backend without changing frontend URLs.

👉 In short:
This block tells Nginx:

“Whenever a request comes to /api/..., drop the /api prefix and forward it to the Flask server running at 127.0.0.1:5000.”

Do you want me to also sketch out how your frontend request would look before and after this Nginx rule?






6th Now we will create an EC2 instance in AWS and generate a PEM file and connect to that EC2 instance with ssh client using gitbash

7th Now we need to transfer our whole model to our server so for that an easy way is to use WINSCP so we will connect to our instance using winscp as 
host: ec2-16-171-25-63.eu-north-1.compute.amazonaws.com 
user: master
password: Advance -> authentication -> .pem -> .ppk

Now we can easily drag and drop our project folder to server from our local machine

8th now using gitbash in our server we will install nginx by command sudo apt-get install nginx

9th we will again set up nginx that which html file to render when the url is called, but this time it got a different path cd /etc/nginx/nginx.conf then within that we will look for virtual host rendering and update our html instead of default one

10th same we modified the nginx.conf in our local system we will modify it in our server system also, here instead of modifying conf file we will create a new conf file with our required details.



server {
    listen 80;
    server_name _;

    # Point to your built frontend files
    root /home/ubuntu/RealState_Project/Client;
    index app.html;

    # Serve the frontend
    location / {
        try_files $uri /app.html;
    }

    # Proxy backend API calls to Flask
    location /api/ {
    rewrite ^/api(/.*)$ $1 break;
    proxy_pass http://127.0.0.1:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
        }
}

11th In Backend I updated the url I was hitting i.e from //var url = "http://127.0.0.1:5000/get_location_names" 
							//var url = "/api/get_location_names";

			to 				var url = "http://ec2-16-171-25-63.eu-north-1.compute.amazonaws.com/api/get_location_names"

because when we configured our nginx in our local system then you remember when we used to type localhost then our webapp used to get loaded so similarly here instead of localhost this is our host name ec2-16-171-25-63.eu-north-1.compute.amazonaws.com so in previous case we used localhost/api/get_price_... so similarly we will do ec2-16-171-25-63.eu-north-1.compute.amazonaws.com/api/get_price...

12th Also it was not working because I was having an Adblocker in my website extension

