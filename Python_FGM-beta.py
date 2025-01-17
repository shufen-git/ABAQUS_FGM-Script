from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import numpy as np
import os
from abaqusConstants import *
################################## Set working directory #############################################

os.chdir(r"C:\Temp\JMEP")

###################################  VERY IMPORTANT ##################################

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
BaseDir = os.getcwd()

################################## Create a new model #############################################
a=0.01
b=0.03
l=0.06
t=b-a
le=20

def CreateModel(variables):
	f0=variables[0]
	n=variables[1]
	Ta=20
	Tb=variables[2]

	# #Al1100
	
	Em=69e9
	num=0.34
	km=220
	alpham=23.6e-6
	sm=150e6

 	# #SiC

	Ec=440e9
	nuc=0.17
	kc=100
	alphac=4.3e-6
	q=91.6e9

	r=np.linspace(a,b,le)
	f=f0 * (((r-a)/t))**n


	E=(((1-f)*Em*((q+Ec) / (q+Em))) + f*Ec) / (((1-f)*((q+Ec) / (q+Em))) + f)
	s=sm*((1-f) + (((q+Em) / (q+Ec))*f*Ec/Em))
	alpha=alpham*(1-f) + alphac*f
	nu=num*(1-f) + nuc*f
	k=km*(1-f) + kc*f


	Efgm =[[E[i],nu[i],r[i]] for i in range(le)]
	alphafgm=[[alpha[i],r[i]] for i in range(le)]
	kfgm=[[k[i],r[i]] for i in range(le)]
	syfgm=[[s[i],0,r[i]] for i in range(le)]


	Mdb()

	mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
	mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
		viewStyle=AXISYM)
	mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(0.0, 
		-0.5), point2=(0.0, 0.5))
	mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
		mdb.models['Model-1'].sketches['__profile__'].geometry[2])
	mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(a, 0.0), 
		point2=(b, l))
	mdb.models['Model-1'].Part(dimensionality=AXISYMMETRIC, name='Part-1', type=
		DEFORMABLE_BODY)
	mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
		mdb.models['Model-1'].sketches['__profile__'])
	del mdb.models['Model-1'].sketches['__profile__']

	########################## Material properties ###########################

	mdb.models['Model-1'].Material(name='Material-1')
	mdb.models['Model-1'].materials['Material-1'].UserDefinedField()
	mdb.models['Model-1'].materials['Material-1'].Elastic(dependencies=1,table=Efgm)
	mdb.models['Model-1'].materials['Material-1'].Conductivity(dependencies=1,table=kfgm)
	mdb.models['Model-1'].materials['Material-1'].Expansion(dependencies=1, table=alphafgm)
	mdb.models['Model-1'].materials['Material-1'].Plastic(dependencies=1, table=syfgm)
	mdb.models['Model-1'].materials['Material-1'].Depvar(n=7)
	######################## SectionAssignment ################################

	mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
		'Section-1', thickness=None)
	mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
		offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
		faces=mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(
		mask=('[#1 ]', ), )), sectionName='Section-1', thicknessAssignment=
		FROM_SECTION)

	################################ Assembly #################################

	mdb.models['Model-1'].rootAssembly.DatumCsysByThreePoints(coordSysType=
		CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 
		0.0, -1.0))
	mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
		part=mdb.models['Model-1'].parts['Part-1'])
	################################ Steps ####################################

	maxincrement=0.01

	mdb.models['Model-1'].CoupledTempDisplacementStep(amplitude=RAMP, cetol=None, 
		creepIntegration=None, deltmx=None, initialInc=0.01, maxInc=0.01, 
		maxNumInc=1000, name='Heating', previous='Initial', response=STEADY_STATE)
	mdb.models['Model-1'].CoupledTempDisplacementStep(amplitude=RAMP, cetol=None, 
		creepIntegration=None, deltmx=None, initialInc=0.01, maxInc=0.01, 
		maxNumInc=1000,name='Cooling', previous='Heating', 
		response=STEADY_STATE)

	############################ Boundary conditions ##############################


	mdb.models['Model-1'].YsymmBC(createStepName='Initial', localCsys=None, name=
		'BC-1', region=Region(
		edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.025, 0.0, 0.0), ), )))

	mdb.models['Model-1'].TemperatureBC(amplitude=UNSET, createStepName='Heating', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=Ta, name='Ta', 
		region=Region(
		edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.01, 0.015, 0.0), ), )))	

	mdb.models['Model-1'].TemperatureBC(amplitude=UNSET, createStepName='Heating', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=Tb, name='Tb'
		, region=Region(
		edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.03, 0.045, 0.0), ), )))

	mdb.models['Model-1'].TemperatureBC(amplitude=UNSET, createStepName='Cooling', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=20.0, name=
		'Tbcooled', region=Region(
		edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.03, 0.045, 0.0), ), )))

	mdb.models['Model-1'].boundaryConditions['Tb'].deactivate('Cooling')

	################################ Mesh ###############################################
	meshradial=50
	meshlength=20
	bias=5

	mdb.models['Model-1'].parts['Part-1'].seedEdgeByBias(biasMethod=SINGLE, 
		constraint=FINER, end1Edges=
		mdb.models['Model-1'].parts['Part-1'].edges.findAt(((0.015, 0.06, 0.0), ), 
		), number=meshradial, ratio=bias)
	mdb.models['Model-1'].parts['Part-1'].seedEdgeByBias(biasMethod=SINGLE, 
		constraint=FINER, end2Edges=
		mdb.models['Model-1'].parts['Part-1'].edges.findAt(((0.025, 0.0, 0.0), ), )
		, number=meshradial, ratio=bias)
	mdb.models['Model-1'].parts['Part-1'].seedEdgeByNumber(constraint=FINER, edges=
		mdb.models['Model-1'].parts['Part-1'].edges.findAt(((0.01, 0.015, 0.0), ), 
		), number=meshlength)
	mdb.models['Model-1'].parts['Part-1'].seedEdgeByNumber(constraint=FINER, edges=
		mdb.models['Model-1'].parts['Part-1'].edges.findAt(((0.03, 0.045, 0.0), ), 
		), number=meshlength)
	mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
		elemCode=CAX8T, elemLibrary=STANDARD), ElemType(elemCode=CAX6MT, 
		elemLibrary=STANDARD)), regions=(
		mdb.models['Model-1'].parts['Part-1'].faces.findAt(((0.016667, 0.02, 0.0), 
		(0.0, 0.0, 1.0)), ), ))
	mdb.models['Model-1'].parts['Part-1'].generateMesh()

	################################ JOB create ###########################################
	mdb.models['Model-1'].FieldOutputRequest(createStepName='Heating', name=
		'F-Output-1', variables=('S', 'MISES','U','UT','PEEQ', 'NT', 'TEMP', 'FTEMP',
		'HFL', 'HFLA', 'HTL', 'HTLA','RFLE', 'RFL', 'CFL', 'NFLUX', 'RADFL',
		'RADFLA', 'RADTL', 'RADTLA','VFTOT', 'SJD', 'SJDA', 'SJDT', 'SJDTA',
		'WEIGHT', 'FLUXS', 'HBF','SDV'))

	mdb.models['Model-1'].HistoryOutputRequest(createStepName='Heating', name=
		'H-Output-1', variables=('ALLAE', 'ALLCD', 'ALLDMD', 'ALLEE', 'ALLFD', 
		'ALLIE', 'ALLJD', 'ALLKE', 'ALLKL', 'ALLPD', 'ALLQB', 'ALLSE', 'ALLSD', 
		'ALLVD', 'ALLWK', 'ETOTAL', 'FTEMP', 'HFLA', 'HTL', 'HTLA', 'RADFL', 
		'RADFLA', 'RADTL', 'RADTLA', 'VFTOT', 'SJD', 'SJDA', 'SJDT', 'SJDTA', 
		'WEIGHT'))
	################################ JOB create ###########################################
#    subroutine name and path is 'C:\\Temp\\JMEP\\JMEPSDV.for'
	mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
		explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
		memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
		multiprocessingMode=DEFAULT, name='Job-FGM1', nodalOutputPrecision=SINGLE, 
		numCpus=1, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
		# userSubroutine='C:\\Temp\\JMEP\\Jahromi.for', waitHours=0, waitMinutes=0)
		userSubroutine='C:\\Temp\\JMEP\\JMEPSDV.for', waitHours=0, waitMinutes=0)

################################ JOB submit ##########################################

	mdb.jobs['Job-FGM1'].submit(consistencyChecking=OFF)
	mdb.jobs['Job-FGM1'].waitForCompletion()
	print("Model Completed")

def PostProcessing(ModelName):

	CurrentDir = os.getcwd()
	odb = session.openOdb(CurrentDir + '/Job-FGM1.odb')
	start_point = (a,0,0)
	end_point = (b,0,0)
	edge_point1=(a,l,0)
	edge_point2=(b,l,0)

	all_nodes=mdb.models['Model-1'].rootAssembly.instances["Part-1-1"].nodes
	start_node = min(all_nodes, key=lambda node: ((node.coordinates[0]-start_point[0])**2 + 
	
	(node.coordinates[1]-start_point[1])**2 + (node.coordinates[2]-start_point[2])**2))
	end_node = min(all_nodes, key=lambda node: ((node.coordinates[0]-end_point[0])**2 + 
	(node.coordinates[1]-end_point[1])**2 + (node.coordinates[2]-end_point[2])**2))
	session.Path(name='Path-1', type=NODE_LIST, expression=(('PART-1-1', (start_node.label, end_node.label, )), ))
	pth = session.paths['Path-1']
	
	start_node = min(all_nodes, key=lambda node: ((node.coordinates[0]-start_point[0])**2 + 
	(node.coordinates[1]-edge_point1[1])**2 + (node.coordinates[2]-edge_point1[2])**2))
	end_node = min(all_nodes, key=lambda node: ((node.coordinates[0]-edge_point2[0])**2 + 
	(node.coordinates[1]-edge_point2[1])**2 + (node.coordinates[2]-edge_point2[2])**2))
	session.Path(name='Path-2', type=NODE_LIST, expression=(('PART-1-1', (start_node.label, end_node.label, )), ))
	pth2 = session.paths['Path-2']
	
	
	lsteps = mdb.models['Model-1'].steps.keys()
	lsteps.pop(0)
	
	args=["S11","S33","S22","MISES","PEEQ"]
	session.viewports['Viewport: 1'].setValues(displayedObject=odb)

	for ls in range(len(lsteps)):

		x=[" "]*5
		last_frame = len(odb.steps[lsteps[ls]].frames)
		
		for comp in range(len(args)):
			if comp<3:
				session.XYDataFromPath(path=pth, name=lsteps[ls]+args[comp],  includeIntersections=True, 
				pathStyle=PATH_POINTS, numIntervals=10, shape=DEFORMED, 
				labelType=TRUE_DISTANCE,variable= ('S',INTEGRATION_POINT,((COMPONENT,args[comp]), ), ),
				step=ls, frame=last_frame-1)
				x[comp] = session.xyDataObjects[lsteps[ls]+args[comp]]
			if comp==3:
				session.XYDataFromPath(name=lsteps[ls]+args[comp], path=pth, includeIntersections=True, 
				pathStyle=PATH_POINTS, numIntervals=10, shape=DEFORMED, 
				labelType=TRUE_DISTANCE,variable=(('S',INTEGRATION_POINT,((INVARIANT, 'Mises'), )), ),
				step=ls, frame=last_frame-1)
				x[comp] = session.xyDataObjects[lsteps[ls]+args[comp]]
			if comp==4:
				session.XYDataFromPath(name=lsteps[ls]+args[comp], path=pth, includeIntersections=True, 
				pathStyle=PATH_POINTS, numIntervals=10, shape=DEFORMED, 
				labelType=TRUE_DISTANCE,variable=(("PEEQ",INTEGRATION_POINT,)),
				step=ls, frame=last_frame-1)
				x[comp] = session.xyDataObjects[lsteps[ls]+args[comp]]
# Uncomment the line below if it is intended to save ["S11","S33","S22","MISES","PEEQ"] in a text file in a required folder
# Replace the path with your own			
# 		session.writeXYReport(fileName='C:/Users/NIT/Documents/Python Scripts/FGM JMEP/'+ModelName+lsteps[ls]+'.txt',appendMode=OFF,xyData=tuple(x))

	session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('PEEQ', 
	INTEGRATION_POINT), ), nodePick=(('PART-1-1', 1, ('[#1 ]', )), ), )
	session.xyDataObjects.changeKey(fromName='PEEQ (Avg: 75%) PI: PART-1-1 N: 1', toName=ModelName+'Tya')

	session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('PEEQ', 
	INTEGRATION_POINT), ), nodePick=(('PART-1-1', 1, ('[#0 #40000 ]', )), ), )
	session.xyDataObjects.changeKey(fromName='PEEQ (Avg: 75%) PI: PART-1-1 N: 51', toName=ModelName+'Tyb')

	x0 = session.xyDataObjects[ModelName+'Tya']
	x1 = session.xyDataObjects[ModelName+'Tyb']

	
################################ Create Models ######################################
models = []

models.append([0.1,2,202])          # f0=0.1,n=2,Tb=202
# models.append([0.1,3,202])
# models.append([0.1,4,203])

########################### Run models in iteration #################################
for i in models:
	ModelName = "Vo="+str(i[0])+"n="+str(i[1])
	print(ModelName)
	NameFolder = BaseDir+ "/" + "/" + ModelName 
	print(NameFolder)
	os.mkdir(NameFolder)
	os.chdir(NameFolder)
	CreateModel(i)
	PostProcessing(ModelName)

os.chdir(r"C:\Temp\JMEP")
