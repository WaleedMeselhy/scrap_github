FROM teracy/angular-cli as frontendbuilder
RUN mkdir -p /repo_analyzer

COPY ./frontend/angular.json /repo_analyzer/angular.json
COPY ./frontend/package.json /repo_analyzer/package.json
COPY ./frontend/tsconfig.json /repo_analyzer/tsconfig.json
COPY ./frontend/tslint.json /repo_analyzer/tslint.json

WORKDIR /repo_analyzer
RUN npm install
COPY ./frontend/e2e /repo_analyzer/e2e
COPY ./frontend/src     /repo_analyzer/src
COPY ./frontend/browserslist /repo_analyzer
COPY ./frontend/karma.conf.js /repo_analyzer
COPY ./frontend/package-lock.json /repo_analyzer
COPY ./frontend/tsconfig.app.json /repo_analyzer
COPY ./frontend/tsconfig.spec.json /repo_analyzer
RUN ng build --prod
FROM nginx:alpine
ENV DEBIAN_FRONTEND noninteractive


# Setup nginx
COPY ./frontend/nginx.conf /etc/nginx/nginx.conf
COPY ./frontend/frontend.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf


COPY --from=frontendbuilder /repo_analyzer/dist/git-repos-analyzer /static

