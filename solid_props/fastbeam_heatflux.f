      SUBROUTINE SDVINI(STATEV,COORDS,NSTATV,NCRDS,NOEL,NPT,
     1     LAYER,KSPT)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION STATEV(NSTATV),COORDS(NCRDS)
      STATEV(2) = 0
      RETURN
      END
 
      SUBROUTINE UEXTERNALDB(LOP,LRESTART,TIME,DTIME,KSTEP,KINC)
C
      INCLUDE 'ABA_PARAM.INC'
      
C
      DIMENSION TIME(2)
C

      real, dimension(1000) :: tr,xr,yr,zr,pr
      common /shared/ tr,xr,yr,zr,pr

      INTEGER :: curr_index
      common /ind/ curr_index


      REAL N, zarc, K, curr_z
      DOUBLE PRECISION curr_time, curr_timel
      common /wayf/ curr_time, curr_timel
      INTEGER io, ioo, iooo, ierr
      INTEGER :: nlines_e
      common /linesf/ nlines_e
      INTEGER :: nlines
      INTEGER :: nlines_n
      common /numf/ nlines, nlines_n
      DOUBLE PRECISION topz
      common /blf/ topz
      INTEGER :: nlines_lay
      common /laypf/ nlines_lay
      INTEGER :: count
      common /countf/ count
      
      LOP=0

      IF (MOD(KSTEP,2).EQ.1) THEN 
      	open(53,file='/data2/scooke/interp_laser/laser_pos.txt',
     1	iostat=io,status='old')
      	if (io/=0) stop 'Cannot open file! '

         	nlines = 0
      	do
          	read(53,*,iostat=io)
          	if (io/=0) exit
          	nlines = nlines + 1 
      	end do
          
      	close(53)
      
      	open(68,file='/data2/scooke/interp_laser/laser_pos.txt', 
     1	status='old')

      	do i = 1,nlines
          	read(68,*) tr(i), xr(i), yr(i), zr(i), pr(i)
      	end do     
      	close(68)
      END IF 

      curr_time = tr(1)
      do N=1,nlines
          if(ABS(TIME(1)-tr(N)).LE.ABS(TIME(1)-curr_time)) THEN
              curr_time = tr(N)
              curr_index = N
          end if
      end do   

      RETURN
      END   
    
      SUBROUTINE DFLUX(FLUX,SOL,KSTEP,KINC,TIME,NOEL,NPT,COORDS,JLTYP,TEMP,PRESS,SNAME)
C	  
	  INCLUDE 'ABA_PARAM.INC'
C
	  DIMENSION FLUX(2), TIME(2), COORDS(3)
	  CHARACTER*80 SNAME
C
C	BEAM PARAMETERS, SPEED, SIGMA, CENTER OF BEAM, EFFICIENCY, POWER
          real, dimension(1000) :: tr,xr,yr,zr,pr
          common /shared/ tr,xr,yr,zr,pr

          INTEGER :: curr_index
          common /ind/ curr_index
C	  
	  REAL Pi, Exp
	  REAL Power, Efficiency, Effective_Power, Sigma_X, Sigma_Z, Peak_Flux
	  REAL Speed_Of_Beam
	  REAL Center_Of_BeamX, Center_Of_BeamZ, Processed_Length
	  REAL Bottom_LimitX, Top_LimitX
	  REAL Bottom_LimitZ, Top_LimitZ
	  REAL PositionX, PositionZ
          REAL BeamPowerMax, Brate, Beamini
	  REAL t1,z1,x1,t0,z0,x0,xarc,zarc,bPower,yarc
	  LOGICAL :: Check
C	    
C		
	  bPower = pr(curr_index)

      	  yarc = zr(curr_index)
      	  BeamPowerMax = (pr(curr_index))*1000.d0 

	  Pi = 3.14159265D0
	  Exp = 2.71828183D0
C	  BeamPowerMax = 200000D0
          Beamini = 20000D0
          Brate = 1000000D0
	  IF (BeamPowerMax.LT.0) THEN
	        BeamPowerMax = 0.d0
	  END IF

          Power = Beamini + Brate * TIME(1)
          IF (Power .GE. BeamPowerMax) THEN
                Power = BeamPowerMax

          END IF
	  Efficiency = 0.72D0
	  Effective_Power = BeamPowerMax * Efficiency
	  Sigma_X = 0.145D0
	  Sigma_Z = 0.145D0
	  Sigma_Max = (1 / (((2 * Pi * Sigma_X * Sigma_Z)**0.5)))
          Peak_Flux = (Effective_Power / (((2 * Pi * Sigma_X * Sigma_Z)**0.5)))
          Speed_Of_Beam = 50.D0
	  Processed_Length = Speed_Of_Beam * TIME(1)
	  Start_Of_Beam = xr(0)

C     Interpolation
      Check = False
      IF (TIME(2).GT.tr(curr_index)) THEN
	t1 = tr(curr_index+1)
	x1 = xr(curr_index+1)
	z1 = yr(curr_index+1)
	t0 = tr(curr_index)
	x0 = xr(curr_index)
	z0 = yr(curr_index)
	Check = True
      ELSE IF(TIME(2).LT.tr(curr_index)) THEN
	t1 = tr(curr_index)
	x1 = xr(curr_index)
	z1 = yr(curr_index)
	t0 = tr(curr_index-1)
	x0 = xr(curr_index-1)
	z0 = yr(curr_index-1)
	Check = True
      ELSE
	xarc=xr(curr_index)
      	zarc=yr(curr_index)
	Check = False
      END IF

      IF (CHECK) THEN
	xarc = x0 + (TIME(2)-t0) * (x1-x0)/(t1-t0)
	zarc = z0 + (TIME(2)-t0) * (z1-z0)/(t1-t0)
      ELSE
	xarc=xr(curr_index)
      	zarc=yr(curr_index)
      END IF


C     COORDINATES DEFINED
C
      X = COORDS(1)
      Y = COORDS(2)
      Z = COORDS(3)

      Center_Of_BeamX = xarc
      Center_Of_BeamZ = zarc

      
      PositionX = (X - xarc)
      PositionZ = (Z - zarc)
C	  
C	  
	  Bottom_LimitX = Center_Of_BeamX - 4 * Sigma_X
	  Top_LimitX = Center_Of_BeamX + 4 * Sigma_X
C
	  Bottom_LimitZ = Center_Of_BeamZ - 4 * Sigma_Z
	  Top_LimitZ = Center_Of_BeamZ + 4* Sigma_Z
C
C	NORMAL DISTRIBUTION FLUX DEFINED
C	
      IF (bPower.NE.0) THEN   
      	IF (X.LE.Top_LimitX.AND.X.GE.Bottom_LimitX.AND.Z.LE.Top_LimitZ.AND.Z.GE.Bottom_LimitZ) THEN
C      
		Sigma_Function = (Sigma_Max * Exp**(-1 * ((PositionX)**2/ (2 * Sigma_X * Sigma_X) + ((PositionZ)**2) / (2 * Sigma_Z * Sigma_Z))))
C		
		FLUX(1) = (Sigma_Function) * Peak_Flux
C		
	ELSE
		  FLUX(1) = 0.D0
	END IF
      ELSE
	FLUX(1) = 0.D0
      END IF
C	  
      RETURN
      END