FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend assets
COPY . /usr/share/nginx/html

# Remove the backend folder from the html directory just to keep it clean
RUN rm -rf /usr/share/nginx/html/backend || true

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
