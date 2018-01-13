\Simple Rich to Lean Procedure
\Filename, R2L.mpc
\Date August 14, 2017


\Inputs
#R^Lever	=	1

\Outputs
^Light		=	1
^Hopper		=	2

\DEFINED VARIABLES
\Rich_FR = 5
\Lean_FR = 50
\Rich_count = Number of responses on Rich_FR
\Lean_Count = Number of resps on Lean_FR
\R_Lhold = 15""	--Amount of time that rich ratio must be completed before auto blackout
\L_Lhold = 300""		--Amount of time that lean ratio must be completed before auto blackout
\blackout = 2		--blackout period hold after Sr is deliverd

DIM Data = 

S.S.1,												\Main control logic for FR
	S1,
		#START: ON ^House ---> S2					\Begin State 1

	S2,												\Begine State 2
		5#R^Lever: ON ^Hopper; Z1 ---> SX

S.S.2,												\Response count and display
	S1,
		#START: SHOW 1, RESP, A ---> S2

	S2,
		#R^Lever: ADD A; SHOW 1, RESP, A ---> SX

S.S.3,												\Pellet timer, count, and display
	S1,
		#Z1: ADD B; SHOW 2, PELLETS, B ---> S2
	
	S2,
		0.05": OFF ^Hopper ---> S1

S.S.4,												\Session timer
	S1,
		#START: ---> S2

	S2,
		1': ---> STOPABORT


