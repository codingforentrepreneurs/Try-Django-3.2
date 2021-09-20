[![Try Django 3.2 Logo](https://static.codingforentrepreneurs.com/media/projects/try-django-3-2/images/share/Try_Django_3_2_-_Share.jpg)](https://www.codingforentrepreneurs.com/projects/try-django-3-2)

# Try Django 3.2
Learn the fundamentals behind one of the most popular web frameworks in the world by building a real project.

Learn the fundamentals behind one of the most popular web frameworks in the world by building a real project. Django has so many features that just work out of the box: user authentication, database management, html template rending, URL routing, form data validation, and so much more.

Django is a web-framework written in Python and runs the backend for many of the internet's most popular websites such as Instagram and Pinterest.

Reference code

### Recommended Experience

- [Basic HTML / CSS](https://www.codingforentrepreneurs.com/projects/getting-started-html-css/)
- Python experience such as [30 Days of Python](https://www.codingforentrepreneurs.com/projects/30-days-python-38)


### Deployment

#### Using [doctl](https://kirr.co/usaoez)
1. Reference Post - https://kirr.co/usaoez

2. Sign up for DigitalOcean - https://do.co/cfe-youtube

3. Install doctl - https://kirr.co/dxcc48

4. Get API Token - https://kirr.co/7x8r90

5. Install the new token with:
```
doctl auth init --context main
```
`--context main` is intensional here (it's used later).

6. Clone Repo

```
git clone https://github.com/codingforentrepreneurs/Try-Django-3.2
```
7. Change to your remote
```
git remote set-url origin https://github.com/USERNAME/REPOSITORY.git
```

8. In `.do/app.yaml` update each instance of
```yaml
github:
    branch: production-3
    deploy_on_push: true
    repo: codingforentrepreneurs/Try-Django-3.2
```
to
```yaml
github:
    branch: production-3
    deploy_on_push: true
    repo: USERNAME/REPOSITORY
```

9. Push your code

```
git push origin main
```

10. Use `doctl`

```
doctl apps create --spec .do/app.yaml  --context main
```
Or, my preferred choice as outlined [here](https://kirr.co/usaoez):
```
echo "$(doctl apps create --spec .do/app.yaml  --context main --format ID --no-header)" > app-id.txt 
```