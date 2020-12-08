from ortools.sat.python import cp_model
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

import itertools
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/home.html', posts=posts)


# @bp.route('/home')
# def home():
#     return render_template('blog/home.html')



@bp.route('/index')
def go_to_index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', jdokterUmum=session['jdokterUmum'],
                           jdokterSpesial=session['jdokterSpesial'], jnurse=session['jnurse'],
                           jshift=session['jshift'], jday=session['jday'])


@bp.route('/go_admin')
def go_to_admin():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/admin.html', posts=posts)


@bp.route('/admin', methods=('GET', 'POST'))
def admin():
    print("a")
    if request.method == "POST":

        jdokterUmum = request.form['jdokterUmum']
        jdokterSpesial = request.form['jdokterSpesial']
        jnurse = request.form['jnurse']
        jshift = request.form['jshift']
        jday = request.form['jday']

        if jdokterUmum != "":
            session['jdokterUmum'] = jdokterUmum
        if jdokterSpesial != "":
            session['jdokterSpesial'] = jdokterSpesial
        if jnurse != "":
            session['jnurse'] = jnurse
        if jshift != "":
            session['jshift'] = jshift
        if jday != "":
            session['jday'] = jday

        print("b")
        print("Session: ", session['jdokterUmum'], session['jdokterSpesial'],
              session['jnurse'], session['jshift'], session['jday'])
        return redirect(url_for('blog.admin', jdokterUmum=jdokterUmum,
                                jdokterSpesial=jdokterSpesial, jnurse=jnurse,
                                jshift=jshift, jday=jday, **request.args))
    return render_template('blog/index.html', jdokterUmum=session['jdokterUmum'],
                           jdokterSpesial=session['jdokterSpesial'], jnurse=session['jnurse'],
                           jshift=session['jshift'], jday=session['jday'])


@bp.route('/schedule', methods=('GET', 'POST'))
def schedule():
    if request.method == 'POST':
        # asks user for input
        doctor = request.form['doctor']
        day = request.form['day']
        symptoms = request.form['symptoms']
        req = day.replace('day', '')

# to check whether there is input
        if doctor != "":
            session['doctor'] = doctor
        if day != "":
            session['day'] = day
            session['req'] = req
        if symptoms != "":
            session['symptoms'] = "-"
        else:
            session['symptoms'] = symptoms

        print(doctor, req, day)
        print(session['doctor'], session['req'], session['symptoms'])

        main(True, False, False)
        print('a')
        session['globalT'] = string_output_global

        strSplit = string_output_global.split()



        # get 3 different shifts from continuous string
        checkDay = False
        tempDay = ""
        temp_get_1 = ""
        temp_get_2 = ""
        temp_get_3 = ""
        temp_get_4 = ""
        counter = 0
        length = len(strSplit)
        for x in range(4):
            for y in range(counter, length):
                counter = counter + 1
                if checkDay == False:
                    tempDay = tempDay + strSplit[y] + " "
                    if strSplit[y] == "!":
                        checkDay = True

                if strSplit[y] == "$":
                    break
                if x == 0 and checkDay == True:  # get shift 0
                    temp_get_1 = temp_get_1 + strSplit[y] + " "
                elif x == 1:  # get shift 1
                    temp_get_2 = temp_get_2 + strSplit[y] + " "
                elif x == 2:  # get shift 2
                    temp_get_3 = temp_get_3 + strSplit[y] + " "
                elif x == 3:  # get shift 3
                    temp_get_4 = temp_get_4 + strSplit[y] + " "

        temp_get_1 = temp_get_1.replace("! ", "")

        temp_list1 = []
        temp_list2 = []
        temp_list3 = []
        temp_list4 = []

# get attributes (shift, nurse, doctor) of shift 0
        strSplit = temp_get_1.split();
        counter = 0
        length = len(strSplit)
        for x in range(3):
            temptemp = []
            for y in range(counter, length):
                counter = counter + 1
                if strSplit[y] == "@" or strSplit[y] == "#":
                    break
                temptemp.append(strSplit[y])
                temp_list1.append(temptemp)
        # remove duplicate keys from list
        temp_list1 = list(temp_list1 for temp_list1, _ in itertools.groupby(temp_list1))

        # get attributes (shift, nurse, doctor) of shift 1
        strSplit = temp_get_2.split();
        counter = 0
        length = len(strSplit)
        for x in range(3):
            temptemp = []
            for y in range(counter, length):
                counter = counter + 1
                if strSplit[y] == "@" or strSplit[y] == "#":
                    break
                temptemp.append(strSplit[y])
                temp_list2.append(temptemp)
        # remove duplicate keys from list
        temp_list2 = list(temp_list2 for temp_list2, _ in itertools.groupby(temp_list2))

        # get attributes (shift, nurse, doctor) of shift 2
        strSplit = temp_get_3.split();
        counter = 0
        length = len(strSplit)
        for x in range(3):
            temptemp = []
            for y in range(counter, length):
                counter = counter + 1
                if strSplit[y] == "@" or strSplit[y] == "#":
                    break
                temptemp.append(strSplit[y])
                temp_list3.append(temptemp)
        # remove duplicate keys from list
        temp_list3 = list(temp_list3 for temp_list3, _ in itertools.groupby(temp_list3))

        # get attributes (shift, nurse, doctor) of shift 3
        strSplit = temp_get_4.split();
        counter = 0
        length = len(strSplit)
        for x in range(3):
            temptemp = []
            for y in range(counter, length):
                counter = counter + 1
                if strSplit[y] == "@" or strSplit[y] == "#":
                    break
                temptemp.append(strSplit[y])
                temp_list4.append(temptemp)
        # remove duplicate keys from list
        temp_list4 = list(temp_list4 for temp_list4, _ in itertools.groupby(temp_list4))

        shift1 = ""
        nurse1 = ""
        doctor1 = ""
        shift2 = ""
        nurse2 = ""
        doctor2 = ""
        shift3 = ""
        nurse3 = ""
        doctor3 = ""
        shift4 = ""
        nurse4 = ""
        doctor4 = ""
# combining list to string
        counter = 0
        for li in temp_list1:  # for list 0
            for x in li:
                if counter == 0:
                    shift1 = shift1 + x + " "
                elif counter == 1:
                    nurse1 = nurse1 + x + " "
                elif counter == 2:
                    doctor1 = doctor1 + x + " "
            counter = counter + 1
        counter = 0
        for li in temp_list2:  # for list 2
            for x in li:
                if counter == 0:
                    shift2 = shift2 + x + " "
                elif counter == 1:
                    nurse2 = nurse2 + x + " "
                elif counter == 2:
                    doctor2 = doctor2 + x + " "
            counter = counter + 1
        counter = 0
        for li in temp_list3:  # for list 3
            for x in li:
                if counter == 0:
                    shift3 = shift3 + x + " "
                elif counter == 1:
                    nurse3 = nurse3 + x + " "
                elif counter == 2:
                    doctor3 = doctor3 + x + " "
            counter = counter + 1
        counter = 0
        for li in temp_list4:  # for list 4
            for x in li:
                if counter == 0:
                    shift4 = shift4 + x + " "
                elif counter == 1:
                    nurse4 = nurse4 + x + " "
                elif counter == 2:
                    doctor4 = doctor4 + x + " "
            counter = counter + 1
        print(shift1, nurse1, doctor1)
        print(shift2, nurse2, doctor2)
        print(shift3, nurse3, doctor3)
        print(shift4, nurse4, doctor4)

        session['shift1'] = shift1
        session['nurse1'] = nurse1
        session['doctor1'] = doctor1

        session['shift2'] = shift2
        session['nurse2'] = nurse2
        session['doctor2'] = doctor2

        session['shift3'] = shift3
        session['nurse3'] = nurse3
        session['doctor3'] = doctor3

        session['shift4'] = shift4
        session['nurse4'] = nurse4
        session['doctor4'] = doctor4

        # sends variable to the url
        return redirect(url_for('blog.schedule', doctor=doctor, day=day,
                                globalT=string_output_global,
                                shift1=shift1, nurse1=nurse1, doctor1=doctor1,
                                shift2=shift2, nurse2=nurse2, doctor2=doctor2,
                                shift3=shift3, nurse3=nurse3, doctor3=doctor3,
                                shift4=shift4, nurse4=nurse4, doctor4=doctor4,
                                **request.args))
    return render_template('blog/schedule.html', doctor=session['doctor'],
                           day=session['day'], globalT=session['globalT'],
                           shift1=session['shift1'], nurse1=session['nurse1'],
                           doctor1=session['doctor1'], shift2=session['shift2'],
                           nurse2=session['nurse2'], doctor2=session['doctor2'],
                           shift3=session['shift3'], nurse3=session['nurse3'],
                           doctor3=session['doctor3'], shift4=session['shift4'],
                           nurse4=session['nurse4'], doctor4=session['doctor4'])


string_output_global = ""


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print solutions."""

    def __init__(self, nurse_shifts, num_nurses, doctor_shifts, num_doctors, num_days, num_shifts, num_doctor_general):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._nurse_shifts = nurse_shifts
        self._num_nurses = num_nurses
        self._doctor_shifts = doctor_shifts
        self._num_doctors = num_doctors
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._num_doctor_general = num_doctor_general

    def on_solution_callback(self):
        string_output = ""
        for d in range(self._num_days):
            string_output += ("Day " + str(d) + "\n" + "!")
            string_temp2 = ""
            for s in range(self._num_shifts):
                string_temp2 += ("\tShift " + str(s) + "\n@")
                is_nurse_working = False
                is_doctor_working = False
                string_temp3 = ""
                for n in range(self._num_nurses):
                    if self.Value(self._nurse_shifts[(n, d, s)]):
                        is_nurse_working = True
                        string_temp3 += ("\t\tNurse " + str(n) + " #")
                for n in range(self._num_doctors):
                    if self.Value(self._doctor_shifts[(n, d, s)]):
                        is_doctor_working = True
                        if int(n) > self._num_doctor_general - 1:
                            string_temp3 += (" Doctor " + str(n) + " (Specialist)\n" + "$")
                        else:
                            string_temp3 += (" Doctor " + str(n) + "\n" + "$")
                string_temp2 += string_temp3
            string_output += string_temp2
        self.StopSearch()
        print(string_output)


class SolutionPrinterRequestedDay(cp_model.CpSolverSolutionCallback):
    print("1")
    """Print solutions."""

    def __init__(self, nurse_shifts, num_nurses, doctor_shifts, num_doctors, requested_day, num_shifts,
                 num_doctor_general, num_doctor_special):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._nurse_shifts = nurse_shifts
        self._num_nurses = num_nurses
        self._doctor_shifts = doctor_shifts
        self._num_doctors = num_doctors
        self._day = requested_day
        self._num_shifts = num_shifts
        self._num_doctor_general = num_doctor_general
        self._num_doctor_special = num_doctor_special
        print("2")

    def on_solution_callback(self):
        print("3")
        d = self._day
        string_output = ("Day " + str(d) + "\n" + "!")
        string_temp2 = ""
        for s in range(self._num_shifts):
            print("X")
            string_temp2 += ("\tShift " + str(s) + "\n" + "@")
            is_nurse_working = False
            is_doctor_working = False
            string_temp3 = ""
            for n in range(self._num_nurses):
                print("Y")
                # print("Session: ", session['jdokterUmum'], session['jdokterSpesial'],
                #       session['jnurse'], session['jshift'], session['jday'])
                # print(session['doctor'], session['req'], session['symptoms'])
                print(n, d, s)
                # explain:  n = number of Nurse , s =shift , d = day
                if self.Value(self._nurse_shifts[(n, d, s)]):
                    print("M")
                    is_nurse_working = True
                    string_temp3 += ("\t\tNurse " + str(n) + " #")
                print("N")
            for n in range(self._num_doctors):
                print("Z")
                if self.Value(self._doctor_shifts[(n, d, s)]):
                    is_doctor_working = True
                    if int(n) > self._num_doctor_general - 1:
                        string_temp3 += (" Doctor " + str(n) + " (Specialist)\n" + "$")
                    else:
                        string_temp3 += (" Doctor " + str(n) + "\n" + "$")

            string_temp2 += string_temp3
        string_output += string_temp2
        print("4")
        global string_output_global
        string_output_global = string_output
        self.StopSearch()
        print(string_output)


class SolutionPrinterRequestedDayAndDoc(cp_model.CpSolverSolutionCallback):
    """Print solutions."""

    def __init__(self, nurse_shifts, num_nurses, doctor_shifts, num_doctors, requested_day, num_shifts,
                 num_doctor_general, num_doctor_special, doctor_type):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._nurse_shifts = nurse_shifts
        self._num_nurses = num_nurses
        self._doctor_shifts = doctor_shifts
        self._num_doctors = num_doctors
        self._day = requested_day
        self._num_shifts = num_shifts
        self._num_doctor_general = num_doctor_general
        self._num_doctor_special = num_doctor_special
        self._doctor_type = doctor_type

    def on_solution_callback(self):
        d = self._day
        string_output = ("Day " + str(d) + "\n")
        string_temp2 = ""
        req_checker = False
        for s in range(self._num_shifts):
            string_temp2 += ("\tShift " + str(s) + "\n")
            is_nurse_working = False
            is_doctor_working = False
            string_temp3 = ""
            for n in range(self._num_nurses):
                if self.Value(self._nurse_shifts[(n, d, s)]):
                    is_nurse_working = True
                    string_temp3 += ("\t\tNurse " + str(n))
            for n in range(self._num_doctors):
                if self.Value(self._doctor_shifts[(n, d, s)]):
                    is_doctor_working = True
                    if int(n) > self._num_doctor_general - 1:
                        string_temp3 += (" Doctor " + str(n) + " (Specialist)\n")
                        if (self._doctor_type == "Spesialis"):
                            req_checker = True
                    else:
                        string_temp3 += (" Doctor " + str(n) + "\n")
                        if (self._doctor_type == "Umum"):
                            req_checker = True
            string_temp2 += string_temp3
        string_output += string_temp2
        self.StopSearch()
        if (req_checker == True):
            string_akhir = "We found a match!\n" + string_output
            string_output_global = string_akhir
            print(string_akhir)
        else:
            # global string_output_global
            string_output_global = "Sorry, no schedule match your request, please try for another day."
            print(string_output_global)


def main(printAll, requestDate, requestBoth):
    # printAll = False
    # requestDate = True
    # requestBoth = False

    # if req
    # Variable initialization
    # num_nurses = 5  # int(input("Enter number of nurses:\n"))
    # num_doctor_general = 3  # int(input("Enter number of genral doctors:\n"))
    # num_doctor_special = 2  # int(input("Enter number of specialist doctors:\n"))
    # num_doctors = (num_doctor_general + num_doctor_special)
    # num_shifts = 3  # int(input("Enter number of shifts:\n"))
    # num_days = 7  # int(input("Enter number of days:\n"))

    num_nurses = int(session['jnurse'])
    num_doctor_general = int(session['jdokterUmum'])  # int(input("Enter number of genral doctors:\n"))
    num_doctor_special = int(session['jdokterSpesial'])  # int(input("Enter number of specialist doctors:\n"))
    num_doctors = (num_doctor_general + num_doctor_special)
    num_shifts = int(session['jshift'])  # int(input("Enter number of shifts:\n"))
    num_days = int(session['jday'])  # int(input("Enter number of days:\n"))

    all_nurses = range(num_nurses)
    all_doctors = range(num_doctors)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    # Creates the model.
    model = cp_model.CpModel()

    print("A")

    # Creates shift variables.
    # nurse_shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    nurse_shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                nurse_shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # doctor_shifts[(n, d, s)]: doctor 'n' works shift 's' on day 'd'.
    doctor_shifts = {}
    for n in all_doctors:
        for d in all_days:
            for s in all_shifts:
                doctor_shifts[(n, d, s)] = model.NewBoolVar('shift_dc%id%is%i' % (n, d, s))

    # Adding the constraints
    # Each shift is assigned to exactly one nurse and one doctor in .
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(nurse_shifts[(n, d, s)] for n in all_nurses) == 1)
            model.Add(sum(doctor_shifts[(n, d, s)] for n in all_doctors) == 1)

    for n in all_nurses:
        for d in all_days:
            # Each nurse works at most one shift per day.
            model.Add(sum(nurse_shifts[(n, d, s)] for s in all_shifts) <= 1)

            # Each nurse who works on the last shift
            # will not work on the first shift of the following day
            model.Add(sum([nurse_shifts[(n, d, num_shifts - 1)], nurse_shifts[(n, (d + 1) % num_days, 0)]]) <= 1)

    for n in all_doctors:
        for d in all_days:
            # Each doctor works at most one shift per day.
            model.Add(sum(doctor_shifts[(n, d, s)] for s in all_shifts) <= 1)

            # Each doctor who works on the last shift
            # will not work on the first shift of the following day
            model.Add(sum([doctor_shifts[(n, d, num_shifts - 1)], doctor_shifts[(n, (d + 1) % num_days, 0)]]) <= 1)

    # No specialist doctor will work on the last shift
    for n in range(num_doctors - num_doctor_special, num_doctors):
        for d in all_days:
            model.Add(sum([doctor_shifts[(n, d, num_shifts - 1)]]) == 0)

    print("B")

    # Try to distribute the shifts evenly, so that each nurse and each doctor works
    # min_shifts_per_nurse shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of nurses or by the number of doctors,
    # some nurses and some doctors will be assigned one more shift.
    min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    if num_shifts * num_days % num_nurses == 0:
        max_shifts_per_nurse = min_shifts_per_nurse
    else:
        max_shifts_per_nurse = min_shifts_per_nurse + 1
    for n in all_nurses:
        num_shifts_worked = 0
        for d in all_days:
            for s in all_shifts:
                num_shifts_worked += nurse_shifts[(n, d, s)]
        model.Add(min_shifts_per_nurse <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_nurse)

    min_shifts_per_doctor = (num_shifts * num_days) // num_doctors
    if num_shifts * num_days % num_doctors == 0:
        max_shifts_per_doctor = min_shifts_per_doctor
    else:
        max_shifts_per_doctor = min_shifts_per_doctor + 1
    for n in all_doctors:
        num_shifts_worked = 0
        for d in all_days:
            for s in all_shifts:
                num_shifts_worked += doctor_shifts[(n, d, s)]
        model.Add(min_shifts_per_doctor <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_doctor)
    print("C")
    # Solver
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0


    solution_printer = SolutionPrinter(nurse_shifts, num_nurses, doctor_shifts, num_doctors,
                                       num_days, num_shifts, num_doctor_general)
    solver.SearchForAllSolutions(model, solution_printer)

    if printAll:
        print("fk")
        # solution_printer = SolutionPrinter(nurse_shifts, num_nurses, doctor_shifts, num_doctors,
        #                                    num_days, num_shifts, num_doctor_general)
        # solver.SearchForAllSolutions(model, solution_printer)

    elif requestDate:
        print("D")
        req_day = int(session['req'])

        solution_printer = SolutionPrinterRequestedDay(nurse_shifts, num_nurses, doctor_shifts, num_doctors,
                                                       req_day, num_shifts, num_doctor_general,
                                                       num_doctor_special)
        print("F")
        # solver.SearchForAllSolutions(model, solution_printer)
        solver.SearchForAllSolutions(model, solution_printer)
        print("E")

    elif requestBoth:
        req_doc = str(session['doctor'])
        req_day = int(session['req'])

        solution_printerz = SolutionPrinterRequestedDayAndDoc(nurse_shifts, num_nurses, doctor_shifts, num_doctors,
                                                              req_day, num_shifts,
                                                              num_doctor_general, num_doctor_special, req_doc)
        solver.SearchForAllSolutions(model, solution_printerz)

    def ConstraintChecker():
        for d in all_days:
            for s in all_shifts:
                checker = False
                if (sum(nurse_shifts[(n, d, s)] for n in all_nurses) <= 1):
                    checker = True
                    # print("a" + str(d) + str(s) + str(checker))

        for d in all_days:
            for s in all_shifts:
                checker = False
                if (sum(doctor_shifts[(n, d, s)] for n in all_doctors) <= 1):
                    checker = True
                    # print("b" + str(d) + str(s) + str(checker))

        for n in all_nurses:
            for d in all_days:
                checker = False
                if (sum(nurse_shifts[(n, d, s)] for s in all_shifts) <= 1):
                    checker = True
                    # print("c" + str(d) + str(n) + str(checker))

        for n in all_doctors:
            for d in all_days:
                checker = False
                if (sum(doctor_shifts[(n, d, s)] for s in all_shifts) > 1):
                    checker = True
                    # print("d" + str(n) + str(d) + str(checker))

        # Each nurse who works on the last shift
        # will not work on the first shift of the following day
        for n in all_nurses:
            for d in all_days:
                checker = False
                if (sum([nurse_shifts[(n, d, num_shifts - 1)], nurse_shifts[(n, (d + 1) % 7, 0)]]) <= 1):
                    checker = True
                    # print("e" + str(n) + str(d) + str(checker))

        # Each doctor who works on the last shift
        # will not work on the first shift of the following day
        for n in all_doctors:
            for d in all_days:
                checker = False
                if (sum([doctor_shifts[(n, d, num_shifts - 1)], doctor_shifts[(n, (d + 1) % 7, 0)]]) <= 1):
                    checker = True
                    # print("f" + str(n) + str(d) + str(checker))

        # No specialist doctor will work on the last shift
        for n in range(num_doctors - num_doctor_special, num_doctors):
            for d in all_days:
                checker = False
                if (sum([doctor_shifts[(n, d, num_shifts - 1)]]) == 0):
                    checker = True
                    # print("g" + str(n) + str(d) + str(checker))

        if not checker:
            print("Constraint not satisfied")
        else:
            print("Constraint satisfied")
