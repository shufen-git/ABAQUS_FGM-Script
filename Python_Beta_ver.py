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
a=0.01					# Inner radius
b=0.03					# Outer radius
l=0.06					# Half length of the cylinder
t=b-a					# Thickness

def CreateModel(i):
	
	Ta=20				# Inner wall temperature
	Tb=200				# Outer wall temperature
##########################################################################################
	meshradial=50		# Elements along radial direction
	meshlength=20		# Elements along axial direction
	bias=5				# Bias factor
	maxincrement=0.01	# Increment
##########################################################################################
	model_name = "Model "+str(i)  # Generate model name
	mdb.Model(name=model_name)  # Create model with the generated name
	mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=1.0)
	mdb.models[model_name].sketches['__profile__'].sketchOptions.setValues(
		viewStyle=AXISYM)
	mdb.models[model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, 
		-0.5), point2=(0.0, 0.5))
	mdb.models[model_name].sketches['__profile__'].FixedConstraint(entity=
		mdb.models[model_name].sketches['__profile__'].geometry[2])
	mdb.models[model_name].sketches['__profile__'].rectangle(point1=(a, 0.0), 
		point2=(b, l))
	mdb.models[model_name].Part(dimensionality=AXISYMMETRIC, name='Part-1', type=
		DEFORMABLE_BODY)
	mdb.models[model_name].parts['Part-1'].BaseShell(sketch=
		mdb.models[model_name].sketches['__profile__'])
	del mdb.models[model_name].sketches['__profile__']

	########################## Material properties ###########################

	mdb.models[model_name].Material(name='Material-1')
	mdb.models[model_name].materials['Material-1'].UserDefinedField()
	mdb.models[model_name].materials['Material-1'].Elastic(dependencies=1, table=
		[[69000000000.0, 0.34000000000000002, 0.01], [69000000000.0, 
		0.34000000000000002, 0.011052631578947368], [69000000000.0, 
		0.34000000000000002, 0.012105263157894737], [69000000000.0, 
		0.34000000000000002, 0.013157894736842105], [69000000000.0, 
		0.34000000000000002, 0.014210526315789472], [69000000000.0, 
		0.34000000000000002, 0.015263157894736841], [69000000000.0, 
		0.34000000000000002, 0.016315789473684207], [69000000000.0, 
		0.34000000000000002, 0.017368421052631578], [69000000000.0, 
		0.34000000000000002, 0.018421052631578946], [69000000000.0, 
		0.34000000000000002, 0.019473684210526313], [69000000000.0, 
		0.34000000000000002, 0.020526315789473684], [69000000000.0, 
		0.34000000000000002, 0.021578947368421052], [69000000000.0, 
		0.34000000000000002, 0.022631578947368419], [69000000000.0, 
		0.34000000000000002, 0.023684210526315787], [69000000000.0, 
		0.34000000000000002, 0.024736842105263154], [69000000000.0, 
		0.34000000000000002, 0.025789473684210522], [69000000000.0, 
		0.34000000000000002, 0.026842105263157889], [69000000000.0, 
		0.34000000000000002, 0.027894736842105257], [69000000000.0, 
		0.34000000000000002, 0.028947368421052624], [69000000000.0, 
		0.34000000000000002, 0.029999999999999999]])
	mdb.models[model_name].materials['Material-1'].Conductivity(dependencies=1, 
		table=[[220.0, 0.01], [220.0, 0.011052631578947368], [220.0, 
		0.012105263157894737], [220.0, 0.013157894736842105], [220.0, 
		0.014210526315789472], [220.0, 0.015263157894736841], [220.0, 
		0.016315789473684207], [220.0, 0.017368421052631578], [220.0, 
		0.018421052631578946], [220.0, 0.019473684210526313], [220.0, 
		0.020526315789473684], [220.0, 0.021578947368421052], [220.0, 
		0.022631578947368419], [220.0, 0.023684210526315787], [220.0, 
		0.024736842105263154], [220.0, 0.025789473684210522], [220.0, 
		0.026842105263157889], [220.0, 0.027894736842105257], [220.0, 
		0.028947368421052624], [220.0, 0.029999999999999999]])
	mdb.models[model_name].materials['Material-1'].Expansion(dependencies=1, table=
		[[2.3600000000000001e-05, 0.01], [2.3600000000000001e-05, 
		0.011052631578947368], [2.3600000000000001e-05, 0.012105263157894737], 
		[2.3600000000000001e-05, 0.013157894736842105], [2.3600000000000001e-05, 
		0.014210526315789472], [2.3600000000000001e-05, 0.015263157894736841], 
		[2.3600000000000001e-05, 0.016315789473684207], [2.3600000000000001e-05, 
		0.017368421052631578], [2.3600000000000001e-05, 0.018421052631578946], 
		[2.3600000000000001e-05, 0.019473684210526313], [2.3600000000000001e-05, 
		0.020526315789473684], [2.3600000000000001e-05, 0.021578947368421052], 
		[2.3600000000000001e-05, 0.022631578947368419], [2.3600000000000001e-05, 
		0.023684210526315787], [2.3600000000000001e-05, 0.024736842105263154], 
		[2.3600000000000001e-05, 0.025789473684210522], [2.3600000000000001e-05, 
		0.026842105263157889], [2.3600000000000001e-05, 0.027894736842105257], 
		[2.3600000000000001e-05, 0.028947368421052624], [2.3600000000000001e-05, 
		0.029999999999999999]])
	mdb.models[model_name].materials['Material-1'].Plastic(dependencies=1, table=
		[[150000000.0, 0, 0.01], [150000000.0, 0, 0.011052631578947368], 
		[150000000.0, 0, 0.012105263157894737], [150000000.0, 0, 
		0.013157894736842105], [150000000.0, 0, 0.014210526315789472], 
		[150000000.0, 0, 0.015263157894736841], [150000000.0, 0, 
		0.016315789473684207], [150000000.0, 0, 0.017368421052631578], 
		[150000000.0, 0, 0.018421052631578946], [150000000.0, 0, 
		0.019473684210526313], [150000000.0, 0, 0.020526315789473684], 
		[150000000.0, 0, 0.021578947368421052], [150000000.0, 0, 
		0.022631578947368419], [150000000.0, 0, 0.023684210526315787], 
		[150000000.0, 0, 0.024736842105263154], [150000000.0, 0, 
		0.025789473684210522], [150000000.0, 0, 0.026842105263157889], 
		[150000000.0, 0, 0.027894736842105257], [150000000.0, 0, 
		0.028947368421052624], [150000000.0, 0, 0.029999999999999999]])
	######################## SectionAssignment ################################

	mdb.models[model_name].HomogeneousSolidSection(material='Material-1', name=
		'Section-1', thickness=None)
	mdb.models[model_name].parts['Part-1'].SectionAssignment(offset=0.0, 
			offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
			faces=mdb.models[model_name].parts['Part-1'].faces.getSequenceFromMask(
			mask=('[#1 ]', ), )), sectionName='Section-1', thicknessAssignment=
			FROM_SECTION)

	################################ Assembly #################################

	mdb.models[model_name].rootAssembly.DatumCsysByThreePoints(coordSysType=
			CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 
			0.0, -1.0))
	mdb.models[model_name].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
		part=mdb.models[model_name].parts['Part-1'])
	################################ Steps ####################################

	mdb.models[model_name].CoupledTempDisplacementStep(amplitude=RAMP, cetol=None, 
		creepIntegration=None, deltmx=None, initialInc=0.01, maxInc=maxincrement, 
		maxNumInc=1000, name='Heating', previous='Initial', response=STEADY_STATE)
	mdb.models[model_name].CoupledTempDisplacementStep(amplitude=RAMP, cetol=None, 
		creepIntegration=None, deltmx=None, initialInc=0.01, maxInc=maxincrement, 
		maxNumInc=1000,name='Cooling', previous='Heating', 
		response=STEADY_STATE)

	############################ Boundary conditions ##############################

	mdb.models[model_name].YsymmBC(createStepName='Initial', localCsys=None, name=
		'BC-1', region=Region(
		edges=mdb.models[model_name].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.025, 0.0, 0.0), ), )))

	mdb.models[model_name].TemperatureBC(amplitude=UNSET, createStepName='Heating', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=Ta, name='Ta', 
		region=Region(
		edges=mdb.models[model_name].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.01, 0.015, 0.0), ), )))	

	mdb.models[model_name].TemperatureBC(amplitude=UNSET, createStepName='Heating', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=Tb, name='Tb'
		, region=Region(
		edges=mdb.models[model_name].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.03, 0.045, 0.0), ), )))

	mdb.models[model_name].TemperatureBC(amplitude=UNSET, createStepName='Cooling', 
		distributionType=UNIFORM, fieldName='', fixed=OFF, magnitude=20.0, name=
		'Tbcooled', region=Region(
		edges=mdb.models[model_name].rootAssembly.instances['Part-1-1'].edges.findAt(
		((0.03, 0.045, 0.0), ), )))

	mdb.models[model_name].boundaryConditions['Tb'].deactivate('Cooling')

	################################ Mesh ###############################################

	mdb.models[model_name].parts['Part-1'].seedEdgeByBias(biasMethod=SINGLE, 
		constraint=FINER, end1Edges=
		mdb.models[model_name].parts['Part-1'].edges.findAt(((0.015, 0.06, 0.0), ), 
		), number=meshradial, ratio=bias)
	mdb.models[model_name].parts['Part-1'].seedEdgeByBias(biasMethod=SINGLE, 
		constraint=FINER, end2Edges=
		mdb.models[model_name].parts['Part-1'].edges.findAt(((0.025, 0.0, 0.0), ), )
		, number=meshradial, ratio=bias)
	mdb.models[model_name].parts['Part-1'].seedEdgeByNumber(constraint=FINER, edges=
		mdb.models[model_name].parts['Part-1'].edges.findAt(((0.01, 0.015, 0.0), ), 
		), number=meshlength)
	mdb.models[model_name].parts['Part-1'].seedEdgeByNumber(constraint=FINER, edges=
		mdb.models[model_name].parts['Part-1'].edges.findAt(((0.03, 0.045, 0.0), ), 
		), number=meshlength)
	mdb.models[model_name].parts['Part-1'].setElementType(elemTypes=(ElemType(
		elemCode=CAX8T, elemLibrary=STANDARD), ElemType(elemCode=CAX6MT, 
		elemLibrary=STANDARD)), regions=(
		mdb.models[model_name].parts['Part-1'].faces.findAt(((0.016667, 0.02, 0.0), 
		(0.0, 0.0, 1.0)), ), ))
	mdb.models[model_name].parts['Part-1'].generateMesh()

	################################ JOB create ###########################################
	mdb.models[model_name].FieldOutputRequest(createStepName='Heating', name=
		'F-Output-1', variables=('S', 'MISES','U','UT','PEEQ', 'NT', 'TEMP', 'FTEMP',
		'HFL', 'HFLA', 'HTL', 'HTLA','RFLE', 'RFL', 'CFL', 'NFLUX', 'RADFL',
		'RADFLA', 'RADTL', 'RADTLA','VFTOT', 'SJD', 'SJDA', 'SJDT', 'SJDTA',
		'WEIGHT', 'FLUXS', 'HBF','SDV'))

	mdb.models[model_name].HistoryOutputRequest(createStepName='Heating', name=
		'H-Output-1', variables=('ALLAE', 'ALLCD', 'ALLDMD', 'ALLEE', 'ALLFD', 
		'ALLIE', 'ALLJD', 'ALLKE', 'ALLKL', 'ALLPD', 'ALLQB', 'ALLSE', 'ALLSD', 
		'ALLVD', 'ALLWK', 'ETOTAL', 'FTEMP', 'HFLA', 'HTL', 'HTLA', 'RADFL', 
		'RADFLA', 'RADTL', 'RADTLA', 'VFTOT', 'SJD', 'SJDA', 'SJDT', 'SJDTA', 
		'WEIGHT'))
	################################ JOB create ###########################################
	########### User must provide the name and path to the subroutine #####################

	mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
		explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
		memory=90, memoryUnits=PERCENTAGE, model=model_name, modelPrint=OFF, 
		multiprocessingMode=DEFAULT, name='Job-FGM'+str(i), nodalOutputPrecision=SINGLE, 
		numCpus=1, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
		userSubroutine='C:\\Temp\\JMEP\\JMEPSDV.for', waitHours=0, waitMinutes=0)

################################ JOB submit ##########################################

models=[1,2,3]	# Models as an example
########################### Create  models in iteration #################################
for i in models:
	ModelName = "Model-"+str(i)
	NameFolder = BaseDir+ "/" + "/" + ModelName 
	os.mkdir(NameFolder)
	os.chdir(NameFolder)
	CreateModel(i)
os.chdir(r"C:\Temp\JMEP")