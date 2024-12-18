C    USDFLD Subroutine for implementing properties of functionally graded material (FGM)

	SUBROUTINE USDFLD(FIELD,STATEV,PNEWDT,DIRECT,T,CELENT,
	1 TIME,DTIME,CMNAME,ORNAME,NFIELD,NSTATV,NOEL,NPT,LAYER,
	2 KSPT,KSTEP,KINC,NDI,NSHR,COORD,JMAC,JMATYP,MATLAYO,LACCFLA)
C         
	INCLUDE 'ABA_PARAM.INC'
C
	CHARACTER*80 CMNAME,ORNAME
	CHARACTER*3 FLGRAY(15)
	DIMENSION FIELD(NFIELD),STATEV(NSTATV),DIRECT(3,3),T(3,3),TIME(2)
	DIMENSION ARRAY(15),JARRAY(15),JMAC(*),JMATYP(*),COORD(*)
	DOUBLE PRECISION n,Em,num,km,alpham,sm,Ec,nuc,kc,alphac,q,thickness
	real :: V0,Vc,Vm,E_fgm,alpha_fgm,nu_fgm,k_fgm,sy_fgm
	
C------------------------------Start of USER code----------------------------------------
	r = COORD(1)				! access x, y, z coordinate
	FIELD(1) = r				! define radius as the field variable
C-------------------------- Material properties of metal and ceramic ---------------------------------
	a=0.01
	b=0.03
	thickness=b-a
	V0=0.1
	n=3
	
	Em=69e9
	num=0.34
	km=220
	alpham=23.6D6
	sm=150e6
	
	Ec=440e9
	nuc=0.17
	kc=100
	alphac=4.3e-6
	q=91.6e9

C-------Compute and save the properties of the FGM as state dependent variable-------
	
	Vc= V0*(((r-a)/thickness)**n)
	Vm=(1-Vc)
	E_fgm=(((1-Vc)*Em*((q+Ec) / (q+Em))) + Vc*Ec) / (((1-Vc)*((q+Ec) / (q+Em))) + Vc)
	nu_fgm=num*(1-Vc) + nuc*Vc
	sy_fgm=sm*((1-Vc) + (((q+Em) / (q+Ec))*Vc*Ec/Em))
	alpha_fgm=alpham*(1-Vc) + alphac*Vc
	k_fgm=km*(1-Vc) + kc*Vc

	STATEV(1)=Vc		! SDV1=Volume fraction of ceramic
	STATEV(2)=Vm		! SDV2=Volume fraction of metal
	STATEV(3)=E_fgm		! SDV3=Young's modulus of FGM
	STATEV(4)=nu_fgm	! SDV4=Poisson's ratio of FGM
	STATEV(5)=sy_fgm	! SDV5=Yield stress of FGM
	STATEV(6)=alpha_fgm	! SDV6=Coefficient of thermal expansion of FGM
	STATEV(7)=k_fgm		! SDV7=Conductivity fraction of FGM
	
C---------------------------------------------------------------------------------------

C 	End of USER code

	RETURN
	END
