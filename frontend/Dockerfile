
# Use the official unprivileged Nginx Alpine image
FROM nginxinc/nginx-unprivileged:alpine

# Temporarily become root to update operating-system packages
USER root

# Upgrade installed Alpine packages to available security fixes
RUN apk upgrade --no-cache

# Return to the non-root Nginx user
USER 101

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend application
COPY index.html /usr/share/nginx/html/index.html

# Document the unprivileged Nginx port
EXPOSE 8080

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
