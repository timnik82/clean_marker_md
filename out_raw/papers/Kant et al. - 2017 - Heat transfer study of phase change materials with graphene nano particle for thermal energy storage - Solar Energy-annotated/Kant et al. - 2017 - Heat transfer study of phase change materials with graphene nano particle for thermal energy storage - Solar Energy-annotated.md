## Solar Energy

journal homepage: [www.elsevier.com/locate/solener](http://www.elsevier.com/locate/solener)

# Heat transfer study of phase change materials with graphene nano particle for thermal energy storage

Karunesh Kant a,⇑ , A. Shukla <sup>a</sup> , Atul Sharma <sup>a</sup> , Pascal Henry Biwole b,c

- <sup>a</sup> Rajiv Gandhi Institute of Petroleum Technology, Jais, Amethi, UP, India
- <sup>b</sup>Department of Mathematics and Interactions, University of Nice Sophia-Antipolis, Nice, France
- <sup>c</sup> Mines Paris Tech, PSL Research University, Center for Processes, Renewable Energies and Energy Systems, Sophia Antipolis, France

#### article info

#### Article history: Received 21 January 2017 Received in revised form 27 February 2017 Accepted 6 March 2017 Available online 14 March 2017

Keywords: PCM Graphene nanoparticles Melt fractions Streamlines Melting Fronts

### abstract

The thermal conductivity of commonly used phase change materials (PCM) for thermal energy storage (TES), such as, fatty acids, paraffin etc., is relatively poor, which is one of the main drawbacks for limiting their utility. In the recent past, few attempts have been made to enhance the thermal conductivity of PCM by mixing different additives in the appropriate amount. Graphene nanoparticles, having higher thermal conductivity may be a potential candidate for the same, when mixed appropriately with different PCM. In present study authors have carried out the numerical investigation for the melting of graphene nanoparticles dispersed PCM filled in an aluminum square cavity heated from one side. In this work, the graphene nanoparticles are mixed in three different volumetric ratios (1%, 3%, and 5%), with three different commonly used categories of organic, inorganic and paraffin PCM (namely, Capric Acid, CaCl26H2O, and n-octadecane) to see the effect on melting of composite PCM developed. The resulting transient isotherms, velocity fields, and melting front and melt fractions thus have been deliberated in detail. These results clearly indicate that the addition of graphene nanoparticles increases melting rate but can also hamper the convection heat transfer within large cavities. The study also shows that such enhanced PCM can be effectively used for different TES applications in different fields. The prediction of temperature variation and rate of melting or solidification may be found useful especially for designing such TES devices.

2017 Elsevier Ltd. All rights reserved.

### 1. Introduction

The growth of the civilization in general and global economic growth, in particular, has largely depended on human efforts to efficiently produce, store and convert to a new form. This is deeply motivating research area and requires development efforts from several spheres of engineering, science and technology, and especially from material sciences. TES related research is mainly concentrated towards efficient use of thermal energy, generally, the solar energy but has considerable interest for thermal energy managing in industries too. One of the main concerns in thermal energy management is to practice materials having high energy storage capacity with high reliability and less aging effect. In the recent past there has been huge amount of research efforts devoted to developing such novel materials for variety of applications, such as buildings, textiles, and space heating. These materials are commonly known as PCM, are promising thermal storage materials for storing and discharging bulk amounts of latent heat throughout phase change process [\(Fang et al., 2009; Hasnain, 1998; Kant](#page-9-0) [et al., 2016a; Murat Kenisarin and Mahkamov, 2006](#page-9-0)) with regulated time intervals associated as per energy demand. Though, the criteria for the choice of PCM for a specific application is its melting temperature, but other properties such as the latent heat of fusion, thermal conductivity, thermal stability, density and lower volume change, also play significant role in better designing of a product and therefore these are essential to be considered ([Ling and Poon, 2013; Mehling and Cabeza, 2007](#page-10-0)). Hence, the optimization of material properties as per requirement is quite challenging and novel materials with better efficiency are being continuously explored with time. Additionally, most applications of PCM require high thermal conductivity, though numbers of PCM usually employed lack the same. The lower thermal conductivity of PCM leads to the increase of heat transfer time for the storage materials causing the poor TES system performance. To increase the rate of heat transfer, several experimental and numerical studies have been performed, for enhancing thermal conductivity using metal matrix, metallic fins, thermal conductive

<sup>⇑</sup> Corresponding author. E-mail address: [k1091kant@gmail.com](mailto:k1091kant@gmail.com) (K. Kant).

#### Nomenclature Cp specific heat (Jkg<sup>1</sup> K<sup>1</sup> ) Cpg specific heat of graphene nano-particles (Jkg<sup>1</sup> K<sup>1</sup> dp diameter of nano-particles (m) <sup>g</sup> gravitational acceleration constant (ms<sup>2</sup> <sup>k</sup> thermal conductivity (Wm<sup>1</sup> K<sup>1</sup> H height of cavity (m) kg thermal conductivity of graphene nano-particles (Wm<sup>1</sup> K<sup>1</sup> Lf latent heat of Fusion (Jkg<sup>1</sup> qw heat flux (Wm<sup>2</sup> ) P pressure (Pa) T temperature (K) t time (s) u velocity (ms 1 <sup>v</sup> velocity in y direction (ms<sup>1</sup> W width of aluminum cavity (m) x distance in x direction (m) y distance in y direction (m) q density (kgm<sup>3</sup> ) U volume fraction of nano-particles U<sup>w</sup> weight fraction of nano-particles DT transition temperature (K) m dynamic viscosity of melted PCM (Pas) b thermal expansion coefficient of PCM Subscripts PCM phase change materials NPCM nanoparticle dispersed PCM Solid PCM in solid state Liquid PCM in liquid state

foams, containers with a honeycomb structure, encapsulation, and the emulsification of highly thermal conductive nanoparticles, etc. ([Kibria et al., 2015; Liu et al., 2015; Nurten et al., 2015; Mills et al.,](#page-10-0) [2006\)](#page-10-0). Review by [Khodadadi et al. \(2013\)](#page-9-0), excellently covers numerous aspects of many of these efforts made in recent past to enhance the thermal conductivity of PCM. These studies indicate that the appropriate mixing of nanoparticles and encapsulation, when done together, could be crucial in significantly augmenting the thermal conductivity of the PCM. Few studies have appeared in the recent past on the solidification and melting pure [\(Kant](#page-9-0) [et al., 2016b](#page-9-0)) and of nano-enhanced PCM. The nanoparticledispersed PCM to qualitatively upgrade TES technology could be highly beneficial for many applications, for instance, efficient storage of solar energy [\(Shukla et al., 2017a, 2017b](#page-10-0)), thermal regulation of photovoltaic ([Kant et al., 2016c; Hasan et al., 2015\)](#page-9-0), TES in buildings by applying at one side of container to building envelope, cooling of engines, etc. [\(Hunger et al., 2009; Jradi et al., 2013;](#page-9-0) [Karthikeyan et al., 2014; Salunkhe and Shembekar, 2012; Shi et al.,](#page-9-0) [2014\)](#page-9-0). [Khodadadi and Hosseinizadeh \(2007\)](#page-10-0) carried out a numerical simulation of water as PCM with copper (Cu) nanoparticles using FLUENT software and reported that the accumulation of Cu nanoparticle in water results in the augmentation of thermal conductivity and consequently affects the melt fraction as well. [Arasu](#page-9-0) [and Mujumdar \(2012\)](#page-9-0) carried out a numerical study using the enthalpy-porosity formulation of Al2O3 nanoparticle suspended PCM with different weight ratio in a square container which was heated from the bottom and vertical side while the opposite wall was maintained at constant temperature. The study described that the liquid-solid interface shape and fluid flow mainly subjected to the thickness of the liquid layer, during the advancement of melting. The rate of melting decreases with the increase in the volumetric composition of alumina (Al2O3) for both ways. [Sebti et al. \(2013\)](#page-10-0) conducted a comprehensive numerical investigation to examine heat transfer augmentation in the melting process in the square cavity through dispersion of Cu nanoparticles. Dispersed nanoparticles in PCM caused an upsurge in thermal conductivity compared to conventional PCM, which leads to heat transfer improvement and a higher melting rate. In addition, heat transfer rate in the nanofluid increased and the melting time reduced as the volume concentration of nanoparticles increased. [Dhaidan et al.](#page-9-0) [\(2013b\)](#page-9-0) carried out an experimental and numerical study on CuO nanoparticle suspended PCM within a circular container having a constant heat flux on the surface of the container, including the effect of eccentricity. [Dhaidan et al. \(2013a\)](#page-9-0) carried out similar

research as [Dhaidan et al. \(2013b\)f](#page-9-0)or the square cavity. Melting of alumina (Al2O3) dispersed PCM in a cavity with two different arrangements of heat sources–sink pairs flush-mounted on the upright sidewalls, was investigated numerically by [Ebrahimi and](#page-9-0) [Dadvand \(2015\)](#page-9-0). The impacts of the nanoparticle mixing were analyzed. In all studied cases, the volume fraction of Al2O3 nanoparticles of 2% resulted in the maximum melting rate. These studies indicate the importance of different approaches to upsurge thermal conductivity for efficient utilization of heat energy storage capacity of PCM. [Alshaer et al. \(2015\)](#page-9-0) carried out a numerical study to see the effect of insertion of RT-65 and Nano carbon tubes in carbon foam matrices of dissimilar porosities. [Tasnim et al. \(2015\)](#page-10-0) reported thermal performance of porous latent heat TES system filled with nanophase change material. The outcomes obtained from scale analysis in simplified relationships among different dimensionless parameters. These studies also suggest the importance of adding nanoparticles to upsurge the thermal conductivity of PCM which further enhances heat transfer rate in the storage materials.

Most of the research studies performed so far focussed on investigating the moving boundary problem for a specific geometry and boundary conditions. Studies related to the melt fraction for a PCM storage system with the different volume fraction of nanoparticles are lacking, though these play a significant role in designing a TES. This is the main motivation of the current work. Moreover, graphene has been found to be very high thermal conductive which could be potentially used for enhancing the thermal conductivity of PCM. In the present study, authors have explored the effect of mixing graphene nanoparticles as an additive in different PCM with varying volume fractions of nanoparticles, when kept in an aluminum container. The three different PCM considered for the present study i.e. Capric Acid, CaCl26H2O and n-octadecane (Organic, Inorganic, and Paraffin) which are commonly used for different TES applications, i.e. building application (by applying one side of container at building envelope) [\(Sharma et al., 2013\)](#page-10-0), solar photovoltaic thermal regulation ([Kant et al., 2016b\)](#page-9-0), solar drying application [\(Kant et al., 2016d](#page-9-0)) and solar greenhouse application ([Shukla et al., 2016\)](#page-10-0), etc.

#### 2. Computational model and boundary condition

The dimensions and geometry of computational model for the present study are shown in [Fig. 1](#page-2-0). The nanoparticle dispersed PCM (NPCM) is filled in the enclosure of size 25 mm 25 mm

<span id="page-2-0"></span>Fig. 1. Computational model and dimensions.

and 2.5 mm wide aluminum cavity. The left wall is kept at constant temperature Th = 10 C higher than melting temperature while the other walls are thermally insulated. The Capric acid, CaCl26H2O, and n-octadecane were taken, having graphene nano-particles with four different volume ratios (0%, 1%, 3% and 5%). The initial temperature of the nano PCM is taken to be 5 C lower than melting temperature of PCM and phase transition interval is taken as 1 C, has also taken in several other studies [\(Biwole et al., 2013;](#page-9-0) [Dhaidan et al., 2013a, 2013b\)](#page-9-0). Inner walls of the aluminum container are put at no slip condition, i.e. the velocity of melted NPCM is zero at the walls. The initial pressure is at atmospheric pressure and the initial velocity of NPCM is zero. The thermo-physical properties of PCM and aluminum container are represented in Table 1. The assumptions for the present study are as following:

- (1) The melting of nanoparticle enhanced PCM (NPCM) is Newtonian and incompressible.
- (2) The flow caused due to the melting is laminar and the viscous dissipations, thermal radiation, and three- dimensional convection are negligible.
- (3) Thermophysical properties of PCM are temperature dependent.
- (4) The melting of PCM is conduction and convection controlled.
- (5) The volume change of nano-particles is negligible.

(6) The graphene nanoparticles are homogeneously distributed in the PCM.

It is vital to mention that in the present study two-dimensional model is used and three-dimensional convection is neglected, just for the sake of avoiding mathematical complexity. Moreover, the period of the three-dimensional convection is less short ([Gong](#page-9-0) [and Mujumdar, 1998\)](#page-9-0) when compared with the whole melting process time, therefore the two-dimensional simulation can be considered to be quite realistic.

#### 3. Mathematical formulation

In the aluminum container, heat transfer takes place due to conduction mode of heat transfer only, whereas in the NPCM the heat transfer takes place with the effect of conduction as well as convection and generation of streamlined due to the density difference in liquid and solid phase. In the following, we present mathematical formulations used in the simulation. The heat transfer diffusion equation (Eq. (1)) applies to the solid aluminum container and NPCM. The velocity fields u in Eq. (1) is given by Navier-Stokes equations for incompressible fluids.

qCp @T @<sup>t</sup> <sup>þ</sup> <sup>q</sup>Cp <sup>u</sup> ! rT ¼ r ðkrTÞ ð1Þ

Table 1 Thermo-physical properties of PCMs and aluminum container.

<sup>a</sup> Not applicable due to no phase change for the graphene and aluminum.

<span id="page-3-0"></span>The value of u for solid aluminum container is 0 hence Eq. [\(1\)](#page-2-0) can be written as

qCp @T @<sup>t</sup> <sup>þ</sup> <sup>r</sup> ðkrTÞ ¼ <sup>0</sup> <sup>ð</sup>2<sup>Þ</sup>

Eq. (2) governs pure conductive heat transfer and q Cp and k are the density, specific heat and thermal conductivity of materials respectively. Here the internal heat generation Q is zero.

The pertinent boundary and initial conditions for the temperature field are:

Tð0; y;tÞ ¼ Th ð3Þ

@T @x x¼H <sup>¼</sup> @<sup>T</sup> @y y¼0;H ¼ 0 ð4Þ

Tðx; y; 0Þ ¼ Tini ð5Þ

Transport of nanoparticles and their rejection by the advancing liquid–solid interface are ignored and it was assumed that the graphene nanoparticles are homogenously distributed in the cavity during the melting process. In fact, the nanoparticles affect only the thermo-physical properties of the PCM. The relations for thermo-physical properties of multi-component systems contain a volume fraction; the following relation is used for conversion between the mass fraction and volume fractions of nanoparticles (Uwt to U):

/ <sup>¼</sup> /wtqPCM /wtqPCM þ ð1 /wtÞq<sup>g</sup> ð6Þ

where qPCM and q<sup>g</sup> respectively signify the PCM density and the nanoparticles density. Note that the weight fraction is the same for both phases, although the volume fractions for the liquid and solid phases will change due to the variation of the density of the phase of the PCM. The density of NPCM is given by:

qNPCM ¼ ð1 /ÞqPCM þ /q<sup>g</sup> ð7Þ

qPCMðTÞ ¼ qsolid þ ðqliquid qsolidÞBðTÞ ð8Þ

where q<sup>g</sup> stands for a density of graphene nano-particles. Let Tm be the mean melt temperature and DT the half range of melt temperatures, the value of function B(T) can be written as:

BðTÞ ¼ 0; T < ðTm DTÞ ðT Tm þ DTÞ=ð2DTÞ; ðTm DTÞ 6 ThðTm þ DTÞ 1; T > ðTm þ DTÞ 8 >< >: ð9Þ

where Tm is melting temperature and DT is transition range of PCM. Eq. (9) shows that the value of function B is 0 when the PCM is solid and 1 when it became liquid. The function B linearly raises from 0 to 1 between the two states of PCM ([Biwole et al., 2013\)](#page-9-0). The heat capacity of PCM can be written as

CpPCM ðTÞ ¼ Cpsolid þ ðCpliquid Cpsolid ÞBðTÞ þ LfDðTÞ ð10Þ

where

DðTÞ ¼ e ðTTmÞ<sup>2</sup> <sup>D</sup>T<sup>2</sup> <sup>=</sup> ffiffiffiffiffiffiffiffiffi pDT<sup>2</sup> p ð11Þ

Function D is a Delta function and its value is zero all over excluding the interval [Tm DT, Tm + DT]. It is pinpointed on Tm and its integral is 1. The main role of this function is to distribute the latent heat equally around the mean melting point. The modified heat capacity of NPCM can be written as ([Dhaidan et al.,](#page-9-0) [2013a\)](#page-9-0):

CpNPCM ¼ ð1 /ÞCpPCM þ /Cpg ð12Þ

The thermal conductivity due to the addition of nanoparticle (ko) of NPCM was determined using the model of [Maxwell \(1904\):](#page-10-0)

ko ¼ kPCM kg þ 2kPCM 2/ðkPCM kg Þ kg <sup>þ</sup> <sup>2</sup>kPCM <sup>þ</sup> /ðkPCM kg <sup>Þ</sup> <sup>ð</sup>13<sup>Þ</sup>

The thermal conductivity of the PCM depending on its phase is:

kPCMðTÞ ¼ ksolid þ ðkliquid ksolidÞBðTÞ ð14Þ

The thermal conductivity enhancement due to the thermal dispersion of the NPCM is:

kd <sup>¼</sup> <sup>5</sup> 104 bkn/ðqCpÞPCM ffiffiffiffiffiffiffiffiffiffi BoT qndp s fðT;/Þ ð15Þ

where

<sup>f</sup>ðT; /Þ¼ð2:<sup>8217</sup> <sup>10</sup><sup>2</sup> / <sup>þ</sup> <sup>3</sup>:<sup>917</sup> <sup>10</sup><sup>3</sup> Þ T Tref þ ð3:0669 <sup>10</sup><sup>2</sup> / <sup>3</sup>:<sup>91123</sup> <sup>10</sup><sup>3</sup> Þ ð16Þ

In the above-given equations, Bo is Boltzmann constant, 1.381 <sup>10</sup><sup>23</sup> J/K and dp is the diameter of nanoparticles. The value of b<sup>k</sup> ¼ 8:4407ð100/Þ 1:07304. The kd accounts for Brownian motion, which causes the temperature dependence of the thermal conductivity. The value of correction factor f in the Brownian motion term is defined as the same as for liquid fraction, B(T) in Eq. (9). Accordingly, the effective thermal conductivity of the colloid is the sum of thermal conductivity due to the Brownian motion of nanoparticle and stagnant thermal conductivity:

kNPCM ¼ kd þ ko ð17Þ

It is assumed that the PCM in the liquid phase is a Newtonian fluid. The momentum transfer and energy conservation equations were solved concurrently with the heat transfer diffusion equation. However, to model the phase transition, the momentum conservation equation was modified as follows:

q @ u ! @<sup>t</sup> <sup>þ</sup> <sup>q</sup> <sup>ð</sup><sup>u</sup> ! rÞ u ! l <sup>r</sup><sup>2</sup> <sup>u</sup> ! ¼ rP þ Fb ! þ Fa ! ð18Þ

u ! ð0; yÞ ¼ u ! ðx; 0Þ ¼ u ! ðx; HÞ ¼ u ! ðW; yÞ ¼ 0 ð19Þ

The viscosity of the PCM and nano-particle colloid containing thinned dispersion of small rigid spherical particles is specified by [Brinkman \(1952\)](#page-9-0) as:

<sup>l</sup>NPCM <sup>¼</sup> <sup>l</sup>PCM ð1 /Þ <sup>2</sup>:<sup>5</sup> ð20Þ

In Eq. (18) the force Fb is a buoyancy force which can be given by the Boussinesq approximation:

Fb ! ¼ qliquidð1 bðT TmÞÞ g ! ð21Þ

And the value of additional force Fa

Fa ! ¼ AðTÞ u ! ð22Þ

with the expression of A(T) inspired from the Carman–Koseny relation for porous medium and the expression of r(P) from Darcy's law as presented in Eq. (24) ([Brent et al., 1988; Voller and](#page-9-0) [Prakash, 1987](#page-9-0)):

<sup>A</sup>ðTÞ ¼ <sup>C</sup>ð<sup>1</sup> <sup>B</sup>ðTÞÞ<sup>2</sup> ðB3 <sup>ð</sup>TÞ þ <sup>q</sup><sup>Þ</sup> <sup>ð</sup>23<sup>Þ</sup>

If the flow is laminar, the value of r(P) is:

<sup>r</sup><sup>P</sup> <sup>¼</sup> Cð<sup>1</sup> <sup>B</sup>ðTÞÞ<sup>2</sup> B3 <sup>ð</sup>T<sup>Þ</sup> <sup>u</sup> ! ð24Þ

The value of C is subject to the morphology of the PCM. In this study, C is taken as a constant value 106 ([Biwole et al., 2013](#page-9-0)). This value is chosen randomly high due to high viscosity. Constant q is chosen very low so as to make Eq. [\(23\)](#page-3-0) effective, even when B(T) is zero. The significant value of q was fixed at 10<sup>3</sup> . As soon as the temperature of the NPCM gets higher than Tm + ΔT, the PCM become completely liquid. Therefore, B is 1 and consequently, A and Fa are zero. The value of A(T) increases by the melting process till the force Fa reaches larger than the convection and diffusion terms in Eq. [\(18\)](#page-3-0) and the momentum equation becomes analogous to the Darcy law for fluid flow in a porous medium:

u ! ¼ <sup>K</sup> l rP ð25Þ

where the permeability K is a function of B(T). When B(T) reduces, the velocity field also reduces until it becomes zero when the PCM converts completely to the solid state. At that point, the PCM temperature is inferior to Tm DT. Therefore, B is 0. Eq. [\(23\)](#page-3-0) represents that the value of A(T) becomes very high. Accordingly, all the terms in the momentum conservation equation are controlled by the added force.

#### 4. Computational procedure and model validation

The simultaneous prevailing partial differential equations are solved numerically by using heat transfer and fluid flow module of the commercial software COMSOL 5.0. The thermo-physical properties of NPCM are defined according to temperature, which determines the phase (liquid, mushy, or solid) and nanoparticles concentration (U). The steps of the numerical calculation are discretization of the domain (element, type, and size), defining the time step and relative and absolute tolerances or errors for the convergence conditions of the solution, determining the nonlinear settings for iteration sequences and selecting the appropriate solver techniques. The present model is divided into two domains, one for aluminum container and the second is for NPCM and both have

quad type meshing as shown in Fig. 2. For aluminum domain, minimum and maximum element size is of 6 <sup>10</sup><sup>5</sup> m and 0.003 m respectively, whereas for the NPCM domain we have taken the minimum and maximum element size of 1.05 <sup>10</sup><sup>4</sup> m and 4.5 <sup>10</sup><sup>4</sup> m respectively. The entire model consists of 8277 domain elements and 464 boundary elements. No significant change in the results was observed when using a finer mesh. The time-dependent study carried out by taking constant (Newtonian) iteration techniques having 30,017 numbers, degrees of freedoms with backward differentiation formulas (i.e. Backward Euler) time stepping method. The higher and lower order of backward differentiation principles is 2 and 1 correspondingly having a tolerance of 0.001. The automatic time stepping was considered and a maximum number of iterations for each time step were taken 6 and the damping factor was 0.9.

The calculation from the present simulation model, in terms of melting front, are compared with the calculations done by [Dhaidan](#page-9-0) [et al. \(2013a\)](#page-9-0) and shown in [Fig. 3.](#page-5-0) This comparative study clearly shows that the developed thermal model is in good agreement with the results of an experimental and numerical study carried out by [Dhaidan et al. \(2013a\)](#page-9-0). The thermo-physical properties of PCM and nanoparticle are used for this study is given in [Table 2.](#page-5-0) Such comparative study puts a stringent test of the consistency of our model and its predictions before using it further.

#### 5. Results and discussion

The results obtained in the present study are governed by heat transfer in solid and liquid medium and fluid flow in a liquid medium. As the aluminum container gets heated, the NPCM absorbs energy and start melting, due to heat transfer by conduction and convection. The results of the present study are studied and deliberated under three subsections in the following: In the first section represents the variation of temperature in terms of isotherm and the melting front is described. The variations of the velocity field in terms of streamline are described in the second section. The third section represents the melting rate in terms of variation of melt fraction.

#### 5.1. Isotherms and melting front

Variation of temperature and melting front for CaCl26H2O in different percentages of graphene nanoparticle additive after 5 and 15 min is represented in [Fig. 4.](#page-5-0) The contour plots of color represent temperature variation of NPCM in C. From these figures, it is clear that the diffusion of nanoparticles produces a substantial effect on the melting. For all the volumetric concentrations of graphene nanoparticles, it can perceive that at the early stages of the melting process (see the [Fig. 4](#page-5-0) at t = 5 min) the isothermal lines are parallel to the container which is heated at a constant temperature. This would imply that the conduction mode of heat transfer is dominating. Though, even the very small influence of the convection cause the heat to transfer near the top part of the container and higher amount of PCM is melted there. With increases in time, the heat transfer due to natural convection becomes the prevailing mode of heat transfer, which can also be inferred from the distorted isotherm lines. This leads the heat to traverse from the heated wall towards the top region of the cavity, therefore speed up the melting process in this region. In [Fig. 4](#page-5-0) at 15 min, the melting interface for 5% (vol.) graphene nano-additives is away from the left and right vertical wall as compared to another percentage of graphene nano-additives. The effect is seen due to thermal conductivity enhancement with the graphene nano-additives; hence, the addition of graphene nanoparticles has a positive effect on heat Fig. 2. Meshing of container and NPCM domain. transfer enhancement. From this figure, it can also be perceived

<span id="page-5-0"></span>Fig. 3. Validation of computational model in the term of melting front between the present work and that of [Dhaidan et al. \(2013a\).](#page-9-0)

Table 2 Thermophysical properties of n-octadecane and CuO nanoparticles for validation.

that the solid-liquid interface is more away from the right vertical wall as compared to the left vertical wall. It is due to melted PCM goes upward on the left (heated) side, then downwards on the right side and accumulates on the bottom right part, causing the off-centered effect that is observed in Fig. 4. This is observed as the ratio of convective and conductive heat flux near the right vertical wall is higher in comparison to the left vertical wall as shown in [Fig. 5](#page-6-0). The melted PCM below the un-melted PCM at the bottom wall is ejected towards the vertical walls, as seen in Fig. 4.

For all the volumetric concentrations of graphene nanoparticles, the melting front, which is fairly smooth at the initial stages of the melting process, grows more and more distorted as the time increases. The melting front for CaCl26H2O gets distorted earlier in comparison to Capric acid and n-octadecane as shown in [Fig. 6](#page-6-0) due to its higher thermal conductivity. During the melting progression, natural convection of the liquid phase is established, which causes the hot liquid PCM near the top heated aluminum container to go up and the cold liquid PCM to descend. As a result, the temperature in the upper area of the liquid turns higher than that in the lower region, which leads to speeding up the melting process in the upper part. Therefore, the melting front is more advanced near the upper section of the cavity. [Fig. 6](#page-6-0) shows that the melting

Fig. 4. Variations of temperature (C) and melting front for CaCl26H2O at different percentages of graphene additive after 5 and 15 min.

<span id="page-6-0"></span>Fig. 5. The ratio of convective and conductive heat flux at left and right vertical wall, (a) after 5 min and (b) after 10 min.

Fig. 6. Temperature and melting front of different NPCM with 5% graphene at different time.

rate of CaCl26H2O is high due to its higher thermal conductivity and it gets completely melted after 20 min. The velocity vector near the solid PCM is high due to a higher temperature gradient. The solid PCM absorbs heat and transforms into a liquid state, causing an upward motion of the fluid in the cavity hence there is a generation of streamlined due to changes in phase and temperature and which results in the higher velocity field at the hightemperature gradient.

#### 5.2. Velocity and stream lines

At the onset of melting process, the solid NPCM being in close proximity to the heated aluminum container wall starts changing phase from solid to liquid. At the early stages of the melting process, the NPCM are melted and transfer upward due to buoyancy force as the density of PCM reduces. As the melting is continued there are formations of two semi-identical circulations (eddies) near the upper both corners of the container as shown in Fig. 7. The direction of circulation is clockwise near the upper left corner and anti-clockwise at upper right corner. As the left vertical wall of the container is at a higher temperature as compared to the right vertical wall, therefore, velocity near the left wall is high as compared to the right. As the ratio of convective and conductive heat flux is near the right vertical wall is higher as compared to the left vertical wall as shown in [Fig. 5.](#page-6-0) Therefore, the melting front at the right vertical wall is away as compared to the left vertical wall. The slanted streamlines in Fig. 7 represent the velocity field in solid NPCM that moves downwards due to the melting of NPCM at the lower wall of the aluminum container.

Fig. 8 represents the variation of velocity (vertical component) at line 2 for different NPCM with 5% graphene additives after 20 min. In this Figure, the y-axis represents the velocity variation and x-axis represents the length of horizontal line 2 as shown in [Fig. 1.](#page-2-0) For all three NPCM, the y component of velocity at a certain distance away from the left vertical walls is, while its value is negative in the middle of the cavity. The component of velocity for CaCl26H2O near the left vertical wall side is higher as compared to Capric acid and n-octadacane [\(Biwole et al., 2013\)](#page-9-0). This is due to its higher thermal conductivity which increases heat transfer rate and leads to higher volumetric force differences between liquid and solid PCM. At the right vertical wall side, the y component

Fig. 8. Variation of Velocity (y component) for different NPCMs at 20 min with 5% graphene additiveat line (Arc) 2.

of velocity for n-octadacane is higher because, after 20 min, the melting interface is closer to the vertical wall as compared to other PCM, therefore, the x component of velocity is low and ycomponent is increased. In the middle of the cavity, the unmelted PCM move in the negative y-direction and the negative y component of the velocity is higher for the CaCl26H2O because of its higher melting rate near the bottom horizontal aluminum container. From the Fig. 8, it is also clear that the position of melting interface at line 2 for CaCl26H2O is maximum and minimum

Fig. 7. Velocity field (m/s) and streamline plot of CaCl26H2O for time 10 min with different percentage of graphene.

for n-octadacane at both vertical walls because of its higher melting rate.

Figs. 9–11 represent the variation of velocity (y component) of CaCl26H2O at 20 min with a different volume ratio of graphene at line 3, line 2 and line 1 respectively. From the Figures, it is clear that at the upper side of the cavity, the y component of the velocity is low due to the generations of eddies and therefore, NPCM also moves in the x-direction. At line2, the y-component of NPCM velocity is higher near vertical walls as compared to line 3 as the x-component of the velocity field is less dominating therefore ycomponent higher near the heated vertical wall and lower at the adiabatic vertical wall. At line 1 the positive and negative vertical component of the velocity field has a very low difference in their absolute value. For all the volumetric concentration of graphene, the positive and the negative y component of velocity field for 5% (vol.) graphene additives are lower. This is due to the addition of graphene nanoparticles the density of NPCM increases which produce a considerable effect on volume force.

Fig. 12 represents the variation of velocity (y component) of CaCl26H2O with 5% (vol.) graphene additive at different time instants at line 2. From the Fig. 12, it is clearly shown that initially the velocity of NPCM is zero and it increases near the vertical wall after 5 and 10 min. As the melting starts, the melted NPCM starts moving upwards near the vertical walls and solid NPCM in the middle of cavity moves in downwards (see for 5 min in Fig. 12). Around 10 min, the volume of melted NPCM increases and the positive vertical component of velocity field also increases near the vertical wall. It reaches its highest negative value in between 0.0175 m and 0.020 m of arc length (see for 10 min in Fig. 12). Further, as the time increases, the y component of velocity field decreases as the temperature difference between the heated wall and the NPCM decreases.

### 5.3. Melt fraction

Although the liquid–solid interface images seem identical in [Fig. 4](#page-5-0) for all the volumetric concentration of graphene nanoparticles, though, there are variations between the amounts of melted NPCM as shown in [Fig. 13.](#page-9-0) It can be observed from this figure that the rate of melting increases with the increase in the volumetric concentration of nanoparticles, as expected also. But it is also noticed that this increase in melting rate is quite small in comparison to the melting of pure PCM. This may be explained as follows:

Fig. 9. Variation of velocity (y component) of CaCl26H2O at 20 min with different volume ratios of graphene at line (Arc) 3.

Fig. 10. Variation of velocity (y component) of CaCl26H2O at 20 min with different volume ratios of graphene at line (Arc) 2.

Fig. 11. Variation of velocity (y component) of CaCl26H2O at 20 min with different volume ratios of graphene at line (Arc) 1.

Fig. 12. Variation of velocity (y component) of CaCl26H2O with 5% graphene additive at different time instants at line (Arc) 2.

<span id="page-9-0"></span>Fig. 13. Variations of melt fraction with time.

when the nanoparticles are added to the PCM, its conductivity, as well as viscosity, both is increased. The conductivity increment has a constructive effect although the viscosity augmentation has a negative effect (weakens the buoyancy effect) on the heat transfer and henceforth on the melting progression. At a high volumetric concentration of nanoparticles, the adverse influence of viscosity enhancement may become comparable to the positive effect of conductivity increment of NPCM.

The present study clearly indicates that the importance of adding of the nanoparticle as it leads to enhanced heat transfer of phase change materials. The NPCM can be applied to the various practical applications such as building, thermal regulation of photovoltaic panels, solar drying solar desalination etc. Thermal energy storage devices are installed in several ways in different applications. In the building application, the NPCM can be implemented by direct incorporation, immersion, encapsulation, building materials, false ceiling, flooring, etc. ([Zhou et al., 2012\)](#page-10-0). This study is a preliminary study showing the importance of adding nanoparticles for thermal conductivity enhancement of PCM as well as heat transfer enhancement, taking constant wall temperature. This can be further, improved by considering specific application of NPCM with considering the real solar radiation (which is the first derivative of temperature), wind speed and other ambient conditions.

### 6. Conclusion

PCM and their heat transfer enhancement through nanoengineering are picking up at very fast pace due to its wide range of applications. In such studies, the important aspects to be investigated are preparation and characterization of NPCM, and their dynamics simulation- study to see the overall change in thermophysical properties. The melting of three different PCM filled in an aluminum square cavity subjected to a constant vertical wall temperature is carried out with three dissimilar volumetric concentrations of graphene nanoparticles. It is reported that the addition of the graphene nanoparticles enhances the effective thermal conductivity of the PCM and improves the melting characteristics such as the melting rate. The effect of emulsifying the graphene nanoparticles in PCM results in a relative increase of the dynamic viscosity compared with that of the pure PCM, thus considerably degrading its natural convection heat transfer efficiency with the increased concentration of nanoparticles across the melted region. Based on the present study, it can also be said that the effective thermal conductivity of all three latent heat storage media can be significantly increased by using smaller volumetric concentrations of graphene particles although the convection heat transfer gets hampered by the same additives. This phenomenon may be of concern in large PCM tanks, where PCM melting is usually dominated by convection. Nevertheless, PCM in common and the NPCM in specific, have great potential for the demanding TES applications.

#### References

Alshaer, W.G., Nada, S.A., Rady, M.A., Le Bot, C., Del Barrio, E. Palomo, 2015. Numerical investigations of using carbon foam/PCM/Nano carbon tubes composites in thermal management of electronic equipment. Energy Convers. Manage. 89, 873–884. [http://dx.doi.org/10.1016/j.enconman.2014.10.045.](http://dx.doi.org/10.1016/j.enconman.2014.10.045)

Arasu, A.V., Mujumdar, A.S., 2012. Numerical study on melting of paraffin wax with Al2O3 in a square enclosure. Int. Commun. Heat Mass Transfer 39, 8–16. [http://](http://dx.doi.org/10.1016/j.icheatmasstransfer.2011.09.013) [dx.doi.org/10.1016/j.icheatmasstransfer.2011.09.013](http://dx.doi.org/10.1016/j.icheatmasstransfer.2011.09.013).

Biwole, P.H., Eclache, P., Kuznik, F., 2013. Phase-change materials to improve solar panel's performance. Energy Build. 62, 59–67. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.enbuild.2013.02.059) [enbuild.2013.02.059](http://dx.doi.org/10.1016/j.enbuild.2013.02.059).

[Brent, A.D., Voller, V.R., Reid, K.J., 1988. Enthalpy-porosity technique for modeling](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0020) [convection-diffusion phase change: application to the melting of a pure metal.](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0020) [Numer. Heat Transfer, Part A Appl. 13, 297–318.](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0020)

[Brinkman, H.C., 1952. The viscosity of concentrated suspensions and solutions. J.](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0025) [Chem. Phys. 20, 571](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0025).

Dhaidan, N.S., Khodadadi, J.M., Al-Hattab, T.A., Al-Mashat, S.M., 2013a. Experimental and numerical investigation of melting of NePCM inside an annular container under a constant heat flux including the effect of eccentricity. Int. J. Heat Mass Transf. 67, 455–468. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.ijheatmasstransfer.2013.08.002) [ijheatmasstransfer.2013.08.002.](http://dx.doi.org/10.1016/j.ijheatmasstransfer.2013.08.002)

Dhaidan, N.S., Khodadadi, J.M., Al-Hattab, T.a., Al-Mashat, S.M., 2013b. Experimental and numerical investigation of melting of phase change material/nanoparticle suspensions in a square container subjected to a constant heat flux. Int. J. Heat Mass Transf. 66, 672–683. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.ijheatmasstransfer.2013.06.057) [ijheatmasstransfer.2013.06.057.](http://dx.doi.org/10.1016/j.ijheatmasstransfer.2013.06.057)

Ebrahimi, A., Dadvand, A., 2015. Simulation of melting of a nano-enhanced phase change material (NePCM) in a square cavity with two heat source–sink pairs. Alex. Eng. J. 54, 1003–1017. <http://dx.doi.org/10.1016/j.aej.2015.09.007>.

Fang, G., Li, H., Yang, F., Liu, X., Wu, S., 2009. Preparation and characterization of nano-encapsulated n-tetradecane as phase change material for thermal energy storage. Chem. Eng. J. 153, 217–221. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.cej.2009.06.019) [cej.2009.06.019.](http://dx.doi.org/10.1016/j.cej.2009.06.019)

Gong, Z.-X., Mujumdar, A.S., 1998. Flow and heat transfer in convection-dominated melting in a rectangular cavity heated from below. Int. J. Heat Mass Transf. 41, 2573–2580. [http://dx.doi.org/10.1016/S0017-9310\(97\)00374-8.](http://dx.doi.org/10.1016/S0017-9310(97)00374-8)

Hasan, A., McCormack, S.J., Huang, M.J., Sarwar, J., Norton, B., 2015. Increased photovoltaic performance through temperature regulation by phase change materials: materials comparison in different climates. Sol. Energy 115, 264– 276. [http://dx.doi.org/10.1016/j.solener.2015.02.003.](http://dx.doi.org/10.1016/j.solener.2015.02.003)

Hasnain, S.M., 1998. Review on sustainable thermal energy storage technologies, Part I: heat storage materials and techniques. Energy Convers. Manage. 39, 1127–1138. [http://dx.doi.org/10.1016/S0196-8904\(98\)00025-9.](http://dx.doi.org/10.1016/S0196-8904(98)00025-9)

Hunger, M., Entrop, a.G., Mandilaras, I., Brouwers, H.J.H., Founti, M., 2009. The behavior of self-compacting concrete containing micro-encapsulated phase change materials. Cement Concr. Compos. 31, 731–743. [http://dx.doi.org/](http://dx.doi.org/10.1016/j.cemconcomp.2009.08.002) [10.1016/j.cemconcomp.2009.08.002.](http://dx.doi.org/10.1016/j.cemconcomp.2009.08.002)

Jradi, M., Gillott, M., Riffat, S., 2013. Simulation of the transient behaviour of encapsulated organic and inorganic phase change materials for lowtemperature energy storage. Appl. Therm. Eng. 59, 211–222. [http://dx.doi.org/](http://dx.doi.org/10.1016/j.applthermaleng.2013.05.022) [10.1016/j.applthermaleng.2013.05.022.](http://dx.doi.org/10.1016/j.applthermaleng.2013.05.022)

Kant, K., Shukla, A., Sharma, A., 2016a. Ternary mixture of fatty acids as phase change materials for thermal energy storage applications Karunesh. J. Energy Storage 6, 153–162. <http://dx.doi.org/10.1016/j.est.2016.04.002>.

Kant, K., Shukla, A., Sharma, A., 2016b. Performance evaluation of fatty acids as phase change material for thermal energy storage. J. Energy Storage 6, 153–162. [http://dx.doi.org/10.1016/j.est.2016.04.002.](http://dx.doi.org/10.1016/j.est.2016.04.002)

Kant, K., Shukla, A., Sharma, A., Biwole, P.H., 2016c. Heat transfer studies of photovoltaic panel coupled with phase change material. Sol. Energy 140, 151– 161. [http://dx.doi.org/10.1016/j.solener.2016.11.006.](http://dx.doi.org/10.1016/j.solener.2016.11.006)

Kant, K., Shukla, A., Sharma, A., Kumar, A., Jain, A., 2016d. Thermal energy storage based solar drying systems: a review. Innov. Food Sci. Emerg. Technol. 34, 86– 99. [http://dx.doi.org/10.1016/j.ifset.2016.01.007.](http://dx.doi.org/10.1016/j.ifset.2016.01.007)

Karthikeyan, S., Solomon, G. Ravikumar, Kumaresan, V., Velraj, R., 2014. Parametric studies on packed bed storage unit filled with PCM encapsulated spherical containers for low temperature solar air heating applications. Energy Convers. Manage. 78, 74–80. [http://dx.doi.org/10.1016/j.enconman.2013.10.042.](http://dx.doi.org/10.1016/j.enconman.2013.10.042)

Khodadadi, J.M., Fan, L., Babaei, H., 2013. Thermal conductivity enhancement of nanostructure-based colloidal suspensions utilized as phase change materials for thermal energy storage: a review. Renew. Sustain. Energy Rev. 24, 418–444. <http://dx.doi.org/10.1016/j.rser.2013.03.031>.

- <span id="page-10-0"></span>Khodadadi, J.M., Hosseinizadeh, S.F., 2007. Nanoparticle-enhanced phase change materials (NEPCM) with great potential for improved thermal energy storage. Int. Commun. Heat Mass Transf. 34, 534–543. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.icheatmasstransfer.2007.02.005) [icheatmasstransfer.2007.02.005.](http://dx.doi.org/10.1016/j.icheatmasstransfer.2007.02.005)
- Kibria, M.A., Anisur, M.R., Mahfuz, M.H., Saidur, R., Metselaar, I.H.S.C., 2015. A review on thermophysical properties of nanoparticle dispersed phase change materials. Energy Convers. Manage. 95, 69–89. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.enconman.2015.02.028) [enconman.2015.02.028.](http://dx.doi.org/10.1016/j.enconman.2015.02.028)
- Ling, T.-C.C., Poon, C.-S.S., 2013. Use of phase change materials for thermal energy storage in concrete: an overview. Constr. Build. Mater. [http://dx.doi.org/](http://dx.doi.org/10.1016/j.conbuildmat.2013.04.031) [10.1016/j.conbuildmat.2013.04.031.](http://dx.doi.org/10.1016/j.conbuildmat.2013.04.031)
- Liu, C., Rao, Z., Zhao, J., Huo, Y., Li, Y., 2015. Review on nanoencapsulated phase change materials: preparation, characterization and heat transfer enhancement. Nano Energy 13, 814–826. [http://dx.doi.org/10.1016/j.nanoen.2015.02.016.](http://dx.doi.org/10.1016/j.nanoen.2015.02.016)
- [Maxwell, J.C., 1904. A Treatise on Electricity and Magnetism. Oxford University](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0125) [Press, Cambridge](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0125).
- Mehling, H., Cabeza, L., 2007. Phase change materials and their basic properties. In: Paksoy, H. (Ed.), Thermal Energy Storage for Sustainable Energy Consumption SE-17, NATO Science Series. Springer, Netherlands, pp. 257–277. [http://dx.doi.](http://dx.doi.org/10.1007/978-1-4020-5290-3_17) [org/10.1007/978-1-4020-5290-3\\_17](http://dx.doi.org/10.1007/978-1-4020-5290-3_17).
- Mills, A., Farid, M., Selman, J.R., Al-Hallaj, S., 2006. Thermal conductivity enhancement of phase change materials using a graphite matrix. Appl. Therm. Eng. 26, 1652–1661. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.applthermaleng.2005.11.022) [applthermaleng.2005.11.022](http://dx.doi.org/10.1016/j.applthermaleng.2005.11.022).
- Murat Kenisarin, A., Mahkamov, K., 2006. Solar energy storage using phase change materials. Renew. Sustain. Energy Rev. 6–17. [http://dx.doi.org/10.1016/j.](http://dx.doi.org/10.1016/j.rser.2006.05.005) [rser.2006.05.005.](http://dx.doi.org/10.1016/j.rser.2006.05.005)
- [Nurten,](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0145) S[., Fois, M., Paksoy, H., 2015. Improving thermal conductivity phase change](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0145) [materials—a study of paraffin nanomagnetite composites. Sol. Energy Mater.](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0145) [Sol. Cells 137, 61–67.](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0145)
- Salunkhe, P.B., Shembekar, P.S., 2012. A review on effect of phase change material encapsulation on the thermal performance of a system. Renew. Sustain. Energy Rev. 16, 5603–5616. <http://dx.doi.org/10.1016/j.rser.2012.05.037>.

- Sebti, S.S., Mastiani, M., Mirzaei, H., Dadvand, A., Kashani, S., Hosseini, S.A., 2013. Numerical study of the melting of nano-enhanced phase change material in a square cavity. J. Zhejiang Univ. – Sci. A 14, 307–316. [http://dx.doi.org/10.1631/](http://dx.doi.org/10.1631/jzus.A1200208) [jzus.A1200208.](http://dx.doi.org/10.1631/jzus.A1200208)
- Sharma, A., Shukla, A., Chen, C.R., Dwivedi, S., 2013. Development of phase change materials for building applications. Energy Build. 64, 403–407. [http://dx.doi.](http://dx.doi.org/10.1016/j.enbuild.2013.05.029) [org/10.1016/j.enbuild.2013.05.029.](http://dx.doi.org/10.1016/j.enbuild.2013.05.029)
- Shi, X., Memon, S.A., Tang, W., Cui, H., Xing, F., 2014. Experimental assessment of position of macro encapsulated phase change material in concrete walls on indoor temperatures and humidity levels. Energy Build. 71, 80–87. [http://dx.](http://dx.doi.org/10.1016/j.enbuild.2013.12.001) [doi.org/10.1016/j.enbuild.2013.12.001.](http://dx.doi.org/10.1016/j.enbuild.2013.12.001)
- Shukla, A., Kant, K., Sharma, A., 2017a. Solar still with latent heat energy storage: a review. Innovat. Food Sci. Emerg. Technol. 41, 34–46. [http://dx.doi.org/10.1016/](http://dx.doi.org/10.1016/j.csl.2006.06.005) [j.csl.2006.06.005.](http://dx.doi.org/10.1016/j.csl.2006.06.005)
- Shukla, A., Kant, K., Sharma, A., Biwole, P.H., 2017b. Cooling methodologies of photovoltaic module for enhancing electrical efficiency: a review. Sol. Energy Mater. Sol. Cells 160, 275–286. [http://dx.doi.org/10.1016/j.solmat.2016.10.047.](http://dx.doi.org/10.1016/j.solmat.2016.10.047)
- Shukla, A., Sharma, A., Kant, K., 2016. Solar greenhouse with thermal energy storage: a review. Curr. Sustain./Renew. Energy Rep. 3, 58–66. [http://dx.doi.org/](http://dx.doi.org/10.1007/s40518-016-0056-y) [10.1007/s40518-016-0056-y](http://dx.doi.org/10.1007/s40518-016-0056-y).
- Tasnim, S.H., Hossain, R., Mahmud, S., Dutta, A., 2015. Convection effect on the melting process of nano-PCM inside porous enclosure. Int. J. Heat Mass Transf. 85, 206–210. <http://dx.doi.org/10.1016/j.ijheatmasstransfer.2015.01.073>.
- [Voller, V.R., Prakash, C., 1987. A fixed grid numerical modelling methodology for](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0190) [convection-diffusion mushy region phase-change problems. Int. J. Heat Mass](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0190) [Transf. 30, 1709–1719](http://refhub.elsevier.com/S0038-092X(17)30173-1/h0190).
- Zhou, D., Zhao, C.Y.Y., Tian, Y., 2012. Review on thermal energy storage with phase change materials (PCMs) in building applications. Appl. Energy 92, 593–605. <http://dx.doi.org/10.1016/j.apenergy.2011.08.025>.