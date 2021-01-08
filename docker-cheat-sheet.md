# Building
docker build -t eu.gcr.io/jutebag/jutebag_py:latest .

Note: don't forget the trailing dot!

# Run (local)
docker container run --name web -p 5000:5000 eu.gcr.io/jutebag/jutebag_py:latest 
docker container stop web

docker container logs --tail 100 web

(cleanup)
docker container rm web

# Publishing
docker push eu.gcr.io/jutebag/jutebag_py:latest
