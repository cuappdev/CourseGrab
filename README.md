# CourseGrab

Need to add a course but there are no empty slots? Instead of constantly checking for an open slot throughout the day, adding undue stress to your busy life, let CourseGrab do it for you! Simply enter the course ID of the course you want to enroll in, and we'll send you a notification email when the course opens up!

## Environment Variables

We recommended to use [`direnv`](https://direnv.net).

To get started, run the following:

```bash
cp envrc.template .envrc
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Note: if `python -m venv venv` doesn't work for you, try `python -m virtualenv venv`. 

## Information

This project has been maintained by Cornell AppDev since Spring 2019.

Originally built for BigRed//Hacks 2016 by Chase Thomas and Ning Ning Sun. Visit the original repository [here](https://github.com/nnsun/CourseGrab).
