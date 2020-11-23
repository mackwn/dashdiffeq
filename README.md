<h2>DashDiffeq</h2>
Interactive simple finite differences solver for basic differential equations. 

Contains a home page, and two dashboards (/app2del and /app1dpar). Each dashboards allows users to select different inputs to the heat equation and graphically view the results. 

All the equations are solved using implicit finite difference with a simple two point derviative approximation (at x+h and x-h). 

The equations were developed using the courses notes from MIT Open Courseware course "Numerical Methods for Partical Differential Equations" located here: https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-90-computational-methods-in-aerospace-engineering-spring-2014/numerical-methods-for-partial-differential-equations/.

Access the deployed app at https://dashdiffeq410.herokuapp.com/

<h3>Installation</h3>
Install the requirements in requirements.txt. App was developed with Python 3.6.10. 

<h3>Running the application</h3>
Run the command "python app.py" to start the application. 

<h3>Application Structure</h3>
<ul>
    <li>apps - module containing dash applications<li>
    <ul>
        <li>app1dpar.py - dash application for parabolic 1-d heat equation</li>
        <li>app2del.py - dash application for elliptical 2-d heat equation</li>
    </ul>
    <li>assets - additional css apart from that provided by dash bootstrap</li>
    <li>diffeq</li>
    <ul>
        <li>elliptic.py - contains class for solving 1-d parabolic heat equation</li>
        <li>parabolic.py - contains class for solving 2-d elliptical heat equation</li>
    </ul>
    <li>tests - test suite, focused on testing the differential equation solvers</li>
    <li>abou - home page for the multi-page application</li>
    <li>app.py - create the dash app</li>
    <li>helpers.py - helper functions for rendering some dash components</li>
    <li>index.py - manages the callbacks for rendering multiple pages</li>
    <li>navbar.py</li>
    <li>Procfile - for deployment to Heroku</li>
</ul>