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
git:
    branch: production-3
    repo_clone_url: https://github.com/codingforentrepreneurs/Try-Django-3.2.git
```
to
```yaml
github:
    branch: production-3
    deploy_on_push: true
    repo: USERNAME/REPOSITORY
```
9. Update ENV Secrets
In `.do/app.yaml`, you'll see the `envs` that includes values with the `type: SECRET`. You *must* use a plain-text value when you create this app.

So change:
```yaml
- key: DJANGO_SECRET_KEY
  scope: RUN_AND_BUILD_TIME
  type: SECRET
  value: EV[1:w8aaS/4qnhOJoLOQW4JnsmcjMQWF9Xfv:ZC08ZkUwFhkEzqXYlgtlwh260FWLbe6Zy+c0dqH4nyaqPFDKNF03wFs4D/51604nC0/xkOfDlHf+ldmkzyEsL68S]

```


To
```yaml
  
- key: DJANGO_SECRET_KEY
  scope: RUN_AND_BUILD_TIME
  type: SECRET
  value: wmu@re-x%d-kql&kzs(wo7@t%icu6d@140e0w!!oh^3q_yaw)w
```
- Create one-off secret keys with [this guide](https://www.codingforentrepreneurs.com/blog/create-a-one-off-django-secret-key/)


10. Create app with `doctl`
New to [doctl](https://kirr.co/usaoez)?

```
doctl apps create --spec .do/app.yaml --context main --format "ID"
```
> This will give you an app ID as a response. Something like `78457d4e6-53c2-43e4-afd1-97e701e1ab81`

After it's is complete, we need to replace `.do/app.yaml` to include the encypted keys reference:


11. Get App Spec with `doctl`
```
doctl apps spec get 78457d4e6-53c2-43e4-afd1-97e701e1ab81 > .do/app.yaml  
```
> The `78457d4e6-53c2-43e4-afd1-97e701e1ab81` is the id from the app created in step 10. Need to find the id? Use `doctl apps list --format "Spec.Name, ID"`


12. Commit & Push your code
It's very important that you do step 11 *prior* to commiting any app.yaml code. (It is not important if you do not have keys you'd like to hide)

```
git add .do/app.yaml
git commit -m "Updated app.yaml SECRET keys"
git push origin main
```
