import django
django.setup()
from superuseractions.models import UserHistoryTable as uht, QuickInviteLogs as qsl
from medical.models import Hospital2 as h2 

from medical.forms import AddHospital as ah
from register.forms import AddHospital as add
from django.contrib.auth.models import User
from pproducts.forms import AddPhysician as ap
from pproducts.models import ProductTags as pt, Product as psp, Physician as pn, LinkedProductTags as lpt, ProductImages as pi
from django.forms.models import model_to_dict 
from pproducts.serializers import PhysicianSerializer as sphys, JsonSerializer as js, JSONSerializerField as jsf
from rest_framework.renderers import JSONRenderer
from login.utility_functions import *
from medical.forms import *
from django.template.loader import get_template
from django.template import Context
from login.models import WaitingRoom
from django.utils import timezone
from django.utils import timezone, dateformat
from quickstart.models import quickStartPhysician as qsp, quickStartHospital1 as qsh
from quickstart.forms import QuickStartHospitalInvite as qshi
from quickstart.utility_functions import send_msg_email
from django.contrib.auth import authenticate, logout as logout_user
from quickstart.forms import quickStartPhysicianSimple as qps
from superuseractions.models import UserHistoryTable as uht


f = {'first_name':'Michael','last_name':'Michaels', 'email':'mah@gmail.com','specialty':['15']}
hospital = {
            'id': 25,
            'name': 'Texas Childrens',
            'taxid': '123456789',
            'bankaccount': '67546786543322',
            'routing': '768956498',
            'street': '75 Jackson St',
            'city': 'New York',
            'state': 'NY',
            'zip': '30043',
            'website': 'www.yahoo.com',
            'total_physicians': 30
        }

f = {
    'Tags': 'No description available.',
    'Shoulder': 'Related to the shoulder, which is the joint that connects the arm to the torso and allows for a wide range of motion.',
    'Hip': 'Related to the hip, which is the joint that connects the thigh bone to the pelvis and allows for a wide range of motion.',
    'Knee': 'Related to the knee, which is the joint that connects the thigh bone to the shin bone and allows for bending and straightening of the leg.',
    'Back': 'Related to the back, which is the area of the body that extends from the neck to the pelvis and includes the spine, muscles, and nerves.',
    'Regenerative': 'Related to regenerative medicine, which is the field of medicine that focuses on using the body’s own cells to help heal or replace damaged tissues or organs.',
    'OTC': 'Related to over-the-counter medications, which are drugs that can be purchased without a prescription and are used to treat minor illnesses or symptoms.',
    'Elbow': 'Related to the elbow, which is the joint that connects the upper arm bone to the forearm bone and allows for bending and straightening of the arm.',
    'Ankle': 'Related to the ankle, which is the joint that connects the leg to the foot and allows for a wide range of motion.',
    'Total Knees': 'Related to total knee replacement, which is a surgical procedure in which the entire knee joint is replaced with an artificial joint.',
    'Partial Knees': 'Related to partial knee replacement, which is a surgical procedure in which only the damaged part of the knee joint is replaced with an artificial joint.',
    'Foot': 'Related to the foot, which is the part of the body that connects the leg to the ground and allows for standing, walking, and running.',
    'Leg': 'Related to the leg, which is the part of the body that extends from the knee to the ankle and includes the bones, muscles, and nerves.',
    'Arm': 'Related to the arm, which is the part of the body that extends from the shoulder to the wrist and includes the bones, muscles, and nerves.',
    'Hand': 'Related to the hand, which is the part of the body that connects the arm to the fingers and allows for a wide range of movements, including grasping and manipulating objects.',
    'Wrist': 'Related to the wrist, which is the joint that connects the hand to the forearm and allows for bending and twisting movements of the hand.',
    'Neck': 'Related to the neck, which is the part of the body that connects the head to the torso and includes the spine, muscles, and nerves.',
    'Repair': 'Related to repair, which refers to the process of fixing or restoring something that has been damaged or broken.',
    'Hamstring': 'Related to the hamstring, which is a group of three muscles located at the back of the thigh that are responsible for bending the knee and extending the hip.',
    'Replacement': 'Related to replacement, which refers to the process of replacing something that has been lost or damaged with something else.',
    'Anterior Hip': 'Related to anterior hip replacement, which is a surgical procedure in which the damaged hip joint is replaced through an anterior approach, meaning that the incision is made at the front of the hip rather than the side or back.',
    'Posterior Hip': 'Related to posterior hip replacement, which is a surgical procedure in which the damaged hip joint is replaced through a posterior approach, meaning that the incision is made at the side or back of the hip.',
    'Lumbar': 'Related to Lumbar and its functions.'
}





