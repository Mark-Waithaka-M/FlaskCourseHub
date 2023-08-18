from flask import Blueprint,render_template,redirect,request,url_for,flash,abort

zoom = Blueprint('zoom',__name__)

@zoom.route('/zoom',methods = ['POST','GET'])
def zoomMeeting():
    return render_template('zoom-meeting.html')

@zoom.route('/zoomMeetingDetails',methods = ['POST','GET'])
def zoomMeetingDetails():
    return render_template('zoom-meeting-details.html')