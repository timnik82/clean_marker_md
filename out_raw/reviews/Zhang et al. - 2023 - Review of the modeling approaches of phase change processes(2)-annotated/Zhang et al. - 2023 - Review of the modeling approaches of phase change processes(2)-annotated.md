Contents lists available at [ScienceDirect](www.sciencedirect.com/science/journal/13640321)

# Renewable and Sustainable Energy Reviews

journal homepage: [www.elsevier.com/locate/rser](https://www.elsevier.com/locate/rser) 

# Review of the modeling approaches of phase change processes

Tao Zhang a,b,c , Dongxin Huo <sup>a</sup> , Chengyao Wang <sup>a</sup> , Zhengrong Shi a,b,\*

- <sup>a</sup> *College of Energy and Mechanical Engineering, Shanghai University of Electric Power, Shanghai, 201306, PR China*
- <sup>b</sup> *Shanghai Non-carbon Energy Conversion and Utilization Institute, Shanghai Jiao Tong University, Shanghai, 200240, PR China*
- <sup>c</sup> *School of Mechanical Engineering, Tianjin University, Tianjin, 300072, PR China*

## ARTICLE INFO

*Keywords:*  Phase change material Phase change process Solution method Numerical simulation FLUENT Nanoparticle

#### ABSTRACT

In recent years, phase change materials have played an important role in the field of energy storage because of their flexibility and high efficiency in energy storage and release. However, most phase change processes are unsteady and highly nonlinear. The ways to obtain exact solutions are urgently needed. This study first summarizes the principles and characteristics of different methods to solve the phase transition process, including analytic methods, numerical methods, and CFD numerical methods. After that, the advantages of employing CFD software to simulate the phase change process are discussed, and the solidification and melting models in FLUENT are introduced. In particular, the influences and weights of natural convection and nanoparticles on the solidification/melting processes are revealed and enumerated in detail. Finally, the challenges and future developments in the solution methods, theoretical models, and numerical simulation applications of phase change materials are prospected. This review shows that most of the phase change heat transfer problems are solved by numerical methods. FLUENT is high-precision software commonly used in CFD software, its solidification and melting model is convenient to simulate the phase change process. Both natural convection and nanoparticles can shorten the melting time of phase change materials.

# **1. Introduction**

The energy crisis is one of the major challenges facing the world today with the transformation and upgrading of the global industry in the new era and the continuous depletion of fossil energy. At present, the main ways to relieve the contradictions between energy supply and energy demand are to develop renewable energy and improve energy utilization rates. Renewable energy mainly includes solar energy, wind energy, water energy, nuclear energy, etc. However, the further utilization and development of renewable energy sources are limited due to the high development costs, uneven distribution, and susceptibility to regional influences, so it is especially vital to improve their energy utilization rates.

Phase change materials (PCMs) are also well-known as phase change energy storage materials. Through phase change, it may release and absorb considerable latent heat without changing the temperature. PCMs have the advantages of small size, a wide range of phase change temperatures, high thermal storage density, and energy stability, and it is very popular in improving energy utilization, developing renewable energy, and improving energy structure. Meanwhile, they are seriously concerned in many fields such as solar energy, building energy saving, textiles and clothing, etc.

One criterion to determine whether a PCMs may be used in practical applications is the melting/solidification rate during the phase transition process [\[1\]](#page-24-0). Since the phase change processes of PCMs are non-stationary heat transfer and the processes are relatively complex, numerical methods have been applied by many studies to solve the phase transition problems. The most popular numerical methods for solving phase transition problems are the enthalpy method and the equivalent heat capacity method [[2](#page-24-0)].

The use of numerical simulation software can better predict the phase change phenomena and realize specific calculations as computer performance improves. Its advantages in low cost, high efficiency and convenience are greatly suggested in obtaining the analytical solution of the highly nonlinear change process of PCMs.

In recent years, there are many reviews of PCMs and the phase transition process, and they have made great contributions. Such as, Wang et al. [\[3\]](#page-24-0) reviewed the stability, photothermal conversion efficiency, and heat transfer optimization of PCM applied to water heaters, as well as the application of PCM in different types of water heaters. Rashid et al. [[4](#page-24-0)] reviewed the research on the effects of the magnetic

<sup>\*</sup> Corresponding authors. College of Energy and Mechanical Engineering, Shanghai University of Electric Power, Shanghai, 201306, PR China. *E-mail address:* [zhengrongshi@shiep.edu.cn](mailto:zhengrongshi@shiep.edu.cn) (Z. Shi).

field, rotation, tilt angle, and vibration on the melting/solidification process of PCMs and NEPCMs in different geometric enclosures. Beyond that, Cui et al. [[5](#page-24-0)] reviewed the research progress of heat transfer improvement of PCMs by using foam metal in recent years. Niˇzeti´c et al. [[6](#page-24-0)] reviewed the application of nano-enhanced phase change materials and nanofluids in experimental systems and summarized the possible problems in the preparation process.

To sum up, these review articles mainly focus on revealing the applications, influences, or enhancements of PCMs in practical applications. However, none of them focuses on how to realize the decryption, despite governing equations of some models that have been displayed. Compared with these review articles, this study provides a comprehensive summary of the modeling approach to solve the phase change process. In particular, the governing equations, advantages, disadvantages, and application conditions of different methods (analytic, numerical, and CFD) are summarized and discussed. The CFD software and solidification and melting model used in numerical simulations are introduced, and the numerical simulation application of phase change processes, especially the influence of natural convection and nanoparticles on phase change processes, is summarized, including simulation methods, PCMs types and device diagram and other detailed information. Finally, the existing problems in the research and the development trend and focus of future research are pointed out. This study is beneficial for designers to quickly find the solution methods regarding their practical applications, for decision makers to judge the input and output of design calculations, for software developers to clarify the direction of development, and for researchers to find new directions.

#### *1.1. Classifications of PCMs*

There are three ways to classify the PCMs, as shown in [Fig. 1](#page-2-0). The first method divides PCMs into liquid-gas PCMs, solid-solid PCMs, solidgas PCMs, and solid-liquid PCMs according to the phase change mechanism [\[7,8\]](#page-24-0). Among them, solid-liquid PCMs have been widely used in practical engineering applications because of their characteristics of small volume change and great latent heat. The second method is to divide the PCMs according to the heat storage temperature. In general, the operation temperature of the low-temperature PCMs is less than 20 ◦C while that of the medium-temperature PCMs ranges between 20 ◦C–250 ◦C; the operation temperature of high-temperature PCMs is above 250 ◦C [[9](#page-24-0)]. The third method divides PCMs into organic PCMs,

<span id="page-2-0"></span>**Fig. 1.** Classifications of PCMs.

inorganic PCMs, and composite PCMs according to the composition of materials [[10,11](#page-24-0)].

## *1.2. Encapsulation of PCMs*

The encapsulation technologies of PCMs can solve the PCM's leakage, improve PCM's thermal and mechanical stabilities, and improve PCM's thermal conductivity. According to the size, the encapsulated PCM can be categorized into three types: macro-encapsulation (above 1 mm), micro-encapsulation (0–1000 *μ*m), and nanoencapsulation (0–1000 nm) [\[12](#page-24-0)]. Macro-encapsulation is a common method for thermal energy storage applications. The shape of the container consists of spherical [\[13](#page-24-0)], rectangular [[14\]](#page-24-0), tubular [[15\]](#page-24-0), or cylindrical [\[16](#page-24-0)]. Compared with macro-encapsulation, micro-encapsulation has a larger ratio of surface area to volume, and thus a better heat exchange performance [[17,18\]](#page-24-0). Nano-encapsulation is the most stable in structure than macro-encapsulation and micro-encapsulation, and it shows a promising prospect in thermal energy storage applications. In recent years, there have been a number of studies on nano-encapsulated PCMs suspension [\[19](#page-24-0)–21], making it an important research direction in the future.

#### *1.3. Application fields of PCMs*

Influenced by the energy crisis and low carbon requirement, PCMs have received a lot of focus. Some studies [22–[25\]](#page-24-0) have pointed out that the advantages of PCMs are small size, large latent heat, excellent chemical stability, high energy storage density, etc. Until now, PCMs have been widely applied in construction [26–[28\]](#page-24-0), solar energy [29–[31\]](#page-24-0), textile [[32,33](#page-24-0)], industrial waste heat utilization [[34](#page-24-0)[,35](#page-25-0)], electronic devices [\[36](#page-25-0),[37\]](#page-25-0), agriculture [\[38](#page-25-0)], food packaging [[39,40](#page-25-0)], aerospace [[41\]](#page-25-0), and other fields [\[42](#page-25-0)–46]. [Table 1](#page-3-0) introduces some application fields and the main research contents of PCMs.

# **2. The solution methods of phase change heat transfer**

Modeling phase change heat transfer is represented by a nonlinear equation of systems, and the phase change heat transfer problem is often called the "moving boundary" problem [[56\]](#page-25-0). Phase change heat transfer has been studied for more than 150 years, starting with the initial study of phase change heat transfer in semi-infinite objects. At present, the methods for solving the phase transition problem are analytic method (accurate analysis, approximate analysis), numerical method (frontier tracking method, fixed frontier method, and fixed grid method), and the CFD numerical method is also particularly important, as shown in [Fig. 2](#page-5-0).

Due to the changes in thermophysical properties during the phase change process and other uncertain factors such as the volume change caused by phase transition and the natural convection that occurs in the liquid phase region, the phase change heat transfer in a limited area cannot be solved accurately. It is difficult to obtain approximate analytical solutions for the multidimensional phase transition processes. Therefore, most of the current phase-change heat transfer problems rely more on numerical methods to solve. The fixed grid method not only solves the solution regions of different phase states as a whole without tracking the locations of their solid-liquid two-phase interfaces but also presents good flexibility to be applied to multi-dimensional and multiinterface situations, so it is widely used.

#### *2.1. Analytic methods*

Analytic methods can be divided into accurate analysis and approximate analysis. The accurate analysis consists of the Neumann method, extended Neumann method, Lightfoot integral method, and Paterson method. However, because of the complexity of the phase change process, the exact analytical solutions can be obtained only in rare cases. There are many approximate analysis methods, including the heat balance integral method, the quasi-steady state method, the thermal resistance method, the perturbation method, the successive approximation method, and so on. For example, for the general onedimensional phase transition, the approximate analysis method can be applied.

# *2.1.1. Neumann method & extended Neumann method*

The accurate analysis is mainly based on the Neumann method and the extended Neumann method. The Neumann method is a method proposed by Franz Neumann in 1860 to solve the phase transition problem of one-dimensional semi-infinite objects [[57\]](#page-25-0). It is built on the premise that the thermophysical properties of solid PCMs were the same

<span id="page-3-0"></span>**Table 1**  Summary of some application fields of PCMs.

(*continued on next page*)

**Table 1** (*continued* )

(*continued on next page*)

#### <span id="page-5-0"></span>**Table 1** (*continued* )

**Fig. 2.** The solution methods of phase change processes.

as that of liquid PCMs and the thermophysical properties of the two-phase state do not change with temperature. That is, the density of solid PCMs equaled that liquid PCMs. On this basis, the method for solving the most fundamental exact solution of the phase transition is built. Haley et al. [\[58](#page-25-0)] conducted an experimental study on the stable solidification of octadecane cooled from the bottom. The results yielded that the interface locations predicted by the Neumann model matched well with the results of the actual tests.

However, the Neumann method is strictly limited to some idealized problems with constant properties, simple boundaries, and initial conditions in semi-infinite or infinite regions. Fig. 3 shows the solidification problem of a semi-infinite plate.

It is assumed that the thermophysical properties of the solid phase and liquid phase of PCMs are independent of temperature; meanwhile, the initial temperature *Ti* of the liquid phase in semi-infinite phase transition is higher than the phase transition temperature *Tm*. When *t >* 0*,* PCMs at *x* = 0 is suddenly cooled and the cooling temperature *Tw* is maintained lower than the melting point of the material.

The governing equations of temperatures of the solid and liquid phases can be expressed as:

∂*Ts /* ∂*t* = *αs* ⋅ ∂2 *Ts* / ∂*x*<sup>2</sup> *x < s*(*t*) (1)

∂*Tl /* ∂*t* = *αl* ⋅ ∂2 *Tl* / ∂*x*<sup>2</sup> *x > s*(*t*) (2)

The initial conditions and boundary conditions are:

*Ts*(*x,* 0) = *Tl*(*x,* 0) = *Ti t* ≤ 0 (3)

*Ts*(0*, t*) = *Tw x* = 0*, t >* 0 (4)

When *x*→∞*Tl*(*x, t*)→*Ti* (5)

The controlling equations for the interface *s(t)* can be expressed as:

*Ts*(*x, t*) = *Tl*(*x, t*) = *Tm x* = *s*(*t*)*, t >* 0 (6)

*κs* ⋅ ∂*Ts*(*x, t*) */* ∂*x* − *κl* ⋅ ∂*Tl*(*x, t*) */* ∂*x* = *ρ*Δ*hm* ⋅ *ds*(*t*) */ dt* (7)

The accurate solution of one-dimensional semi-infinite plate solidification can be yielded according to the initial conditions, boundary conditions, and interface conditions.

However, in real applications, PCMs with the same density in both solid & liquid phases are practically non-existent, which leads to the fact that the Neumann method is not universal. Later, the Neumann method has been popularized and developed, which enables it a broader ability

**Fig. 3.** Schematic diagram of within the PCMs is in a certain form. Then, integrate the heat conduction the solidification process of a semi-infinite plate.

to solve phase transitions. The promoted Neumann method, namely the extended Neumann method, can solve phase transitions with the following conditions: 1) Phase change problems for PCMs with different densities of solid and fluid phases. 2) Phase change problems under fixed heat flow boundary conditions. 3) Phase change problems are caused by the temperature difference between the PCMs and the wall surface of the container. 4) Phase transition problems in the fuzzy region during phase transition processes.

### *2.1.2. Lightfoot integral method*

MNOzisik ¨ [\[59](#page-25-0)] introduced the Lightfoot integral method, also known as the moving heat source method. The basic description equations for solving the phase change process can be expressed as:

∂2 *T*(*x, t*) <sup>∂</sup>*x*<sup>2</sup> <sup>+</sup> 1 *κ ρL ds*(*t*) *dt <sup>δ</sup>*[*<sup>x</sup>* <sup>−</sup> *<sup>s</sup>*(*t*)] <sup>=</sup> <sup>1</sup> *α* ∂*T*(*x, t*) <sup>∂</sup>*<sup>t</sup>* <sup>0</sup> *<sup>&</sup>lt; <sup>x</sup> <sup>&</sup>lt;* <sup>∞</sup>*, <sup>t</sup> <sup>&</sup>gt;* <sup>0</sup> (8)

*Ts*(*x, t*) = *Ti* = 0 *x* = 0*, t >* 0 (9)

*T*(*x, t*) → *T*<sup>0</sup> *x*→∞*, t >* 0 (10)

*T*(*x, t*) = *T*<sup>0</sup> *x >* 0*, t* = 0 (11)

*T*(*x, t*) = *Tm x* = *s*(*t*) (12)

where *δ*[*x* − *s*(*t*)] is the Dirac function.

This method transforms the heat release (or absorption) at the interface between the solid and liquid phases into a moving heat source (or sink), and thus transforms the phase change heat transfer problem into an integral equation solution at the solid-liquid interface position. This method can ignore the differences in thermophysical properties between the solid phase and liquid phase. Due to the limitations in generalizing to the multidimensional cases and the complexity of the solution, the method is generally applicable to solve infinitely large and one-dimensional phase change heat transfer applications.

## *2.1.3. Paterson method*

Zhang Y et al. [[60\]](#page-25-0) proposed the Paterson method. This method solves the phase transition problems by modeling them in cylindrical coordinates and spherical coordinates. That is, the Paterson method is to construct a function of *r/* ̅̅ *<sup>t</sup>* <sup>√</sup> as a variable to further find its exact solution.

The following two functions can be obtained from the temperature response of a continuous linear heat source in an infinite medium and the temperature response of a continuous spherical heat source in an infinite medium. Similarly, they are solutions of radial one-dimensional heat conduction equations with only 1*/t* as the variable in cylindrical coordinate and spherical coordinate, respectively.

− *Ei r* 2 / 4*at*) = ∫ <sup>∞</sup> *r*<sup>2</sup> */*4*at e*<sup>−</sup> *<sup>η</sup> η dη* ≡ *Ei r*2 / <sup>4</sup>*at*) (13)

( *e*<sup>−</sup> *<sup>r</sup>*<sup>2</sup> */*4*at* ̅̅̅̅ *at* <sup>√</sup> ) / *<sup>r</sup>* <sup>−</sup> <sup>1</sup> 2 ̅̅̅ *<sup>π</sup>* <sup>√</sup> *erfc*( *r* <sup>2</sup> ̅̅̅̅ *at* <sup>√</sup> ) (14)

In practical applications, there are many cylindrical and spherical phase change thermal storage devices, so the Paterson method is paid more attention in solving such phase change problems. At the same time, the Paterson method is also helpful in recognizing and understanding the phase change process of such thermal storage devices. However, the shortcomings of this method are that the thermal conductivity equation of its solution has weak adaptability to the boundary conditions and the scope of constructing the exact solution is limited.

#### *2.1.4. Heat balance integral method*

In 1958, Goodman [[61\]](#page-25-0) first proposed the heat balance integral method. The concrete steps are: First, assume that the temperature field control equation into the phase change region. Finally, solve the movement law at the phase interface through the control equations.

Taking frozen liquid which is initially at its phase transition temperature and occupies half space as an example, the mathematical expression of heat conduction of the solid region can be expressed as [[62\]](#page-25-0):

∂*θ /* ∂*t* = ∂2 *θ* / ∂*x*<sup>2</sup> 0 *< x <* Δ(*t*)*, t >* 0 (15)

The thermal diffusion of Eq. (15) is integrated concerning the space variable and the domain 0 ≤ *x* ≤ Δ(*t*)*,* the heat balance integral equation obtained can be expressed as:

*d dt* ∫ Δ 0 *θdx* <sup>=</sup> <sup>∂</sup>*<sup>θ</sup>* ∂*x* ⃒ ⃒ ⃒ *x*=Δ <sup>−</sup> <sup>∂</sup>*<sup>θ</sup>* ∂*x* ⃒ *x*=0 (16)

where, θ is temperature, *θ* = (*T* − *Tm*)*/*(*Tref* − *Tm*).

This method has been highlighted due to its advantages of a clear physical meaning, a simple solution to the phase change heat transfer problems, and can intuitively reflect the relationship among the physical quantities and sensible heat change law [63–[65\]](#page-25-0). It is now the most popular method in the approximate analysis method. Bell et al. [\[66](#page-25-0)] suggested that the accuracy of the heat balance integral method could be improved by refining the variable temperature.

### *2.1.5. Quasi-steady state method*

The quasi-steady-state method utilizes the *Ste* number as the main criterion for calculations. *Ste* number is a criterion to characterize the ratio of sensible heat and latent heat in the following equation:

*Ste* = *cp*(*Tm* − *T*0) / *L* (17)

when the *Ste* number is far less than 1, the sensible heat is far less than the latent heat in the heat transfer process, and the sensible heat can be ignored, at which time the heat transfer process can be regarded as a quasi-steady state process.

The quasi-steady-state method is suitable for applications whose temperature difference is small and the change of sensible heat has little influence on the heat release or heat absorption at the interface during phase change. Comparatively speaking, the solving process is simple and the form of the solution is concise in the quasi-steady-state method. Ahmad et al. [\[67](#page-25-0)] studied and analyzed the heat transfer process of a phase change wall by the quasi-steady state method.

## *2.1.6. Perturbation method*

When the Ste number is small but cannot be ignored, the *Ste* number is usually taken as a perturbation parameter, and the temperature and phase position are then solved according to the parameter expansion. This solution method is named the perturbation method and is also known as the small parameter expansion method [\[68](#page-25-0)].

The definite solutions of a large number of differential equations encountered in engineering include not only independent and dependent variables but also some parameters that reflect the characteristics of the problem itself. Takes the *Ste* number in a phase change process as an example, its value is usually relatively small and therefore is often called a small parameter and can be expressed by *ε*. Accordingly, the solution of the differential equations depends not only on the independent variable but also on the small parameter *ε*. For the heat conduction problem, the temperature distribution in the object will be a function of radial quantity *r*, time *τ*, and small parameter *ε*; that is, *t* = *t*(*r, τ, ε*), which is abbreviated as:

*t* = *tε*(*r, τ*) (18)

The small parameter *ε* can be included in the low-order derivative term (right-hand term) of the differential equation or the high-order derivative term and it can also appear in the condition of definite solution. This kind of definite solution of differential equation with small

parameters is collectively called a perturbation problem. While *ε* = 0, it is called a degradation problem and its solution is expressed by *t*0. Under certain conditions, the solution *tε*of the perturbation problem can be expressed by the asymptotic power series of the small parameter *ε*, the first term of which is the solution *tε*of the corresponding degenerate, that is:

*tε*(*r, <sup>τ</sup>*) <sup>=</sup> *<sup>t</sup>*0(*r, <sup>τ</sup>*) <sup>+</sup>∑<sup>∞</sup> *i*=1 *εi ti*(*r, τ*) (19)

where *ti*(*r, τ*) is a function to be determined. Eq. (19) is an asymptotic expansion of *tε*(*r, τ*), which is called the asymptotic solution of the perturbation problem. Taking the previous finite term in the series on the right of the equal sign, it becomes an approximate solution to the perturbation problem. If different power terms of *ε* can be retained, different levels of approximate solutions can be obtained:

*tε*(*r, τ*) ∼ *t*0(*r, τ*) (20)

*tε*(*r, τ*) ∼ *t*0(*r, τ*) + *εt*1(*r, τ*) (21)

*tε*(*r, τ*) ∼ *t*0(*r, τ*) + *εt*1(*r, τ*) + *ε*<sup>2</sup> *t*2(*r, τ*) (22)

*tε*(*r, <sup>τ</sup>*) <sup>∼</sup> *<sup>t</sup>*0(*r, <sup>τ</sup>*) <sup>+</sup>∑*<sup>n</sup> i*=1 *εi ti*(*r, τ*) (23)

where the last line is an N-order approximation. *t*0(*r, τ*) is the basic part of *tε*(*r, <sup>τ</sup>*), and ∑*<sup>n</sup> i*=1*ε<sup>i</sup> ti*(*r, τ*) is the perturbation part of *tε*(*r, τ*).

The perturbation method has a higher accuracy but its solution is more tedious. Caldwell et al. [[69\]](#page-25-0) applied the perturbation method to solve one-dimensional Stefan phase change heat transfer with time-varying boundary conditions. Jamal-Abad et al. [\[70](#page-25-0)] revealed the heat transfer patterns within a solar air heat exchanger filled with porous media by using the perturbation method.

#### *2.1.7. Thermal resistance method*

The thermal resistance method was proposed by Chen Zeshao [[71\]](#page-25-0) in 1991 to solve the phase change heat conduction problems. This method assumes that the heat flow is released at the phase interface, its value can be calculated as followed:

*q* = *qL* + *qs* + *ql* (24)

The advantage of the thermal resistance method is that it combines the advantages of the quasi-steady state method with the perturbation method. Thus, it is now highly appreciated due to it simultaneously considers the simplicity of the quasi-steady state method and the high precision of the perturbation method.

## *2.1.8. Successive approximation method*

The successive approximation method can also be regarded as the asymptotic approach method. It does not ignore the governing equation during the solving process but yields the solution with a higher and higher degree of approximation convergence. Its advantages manifest in good convergence and accurate numerical solutions.

This method is to construct the recursive equation of its approximate solution sequence according to the equation, and then prove that the limit of this sequence is a solution of the original equation. For the equation:

*φ*(*x*) = *λ* ∫ *<sup>b</sup> a k*(*x, t*)*φ*(*t*)*dt* + *f*(*x*) (25)

the functions sequence {*φm*(*x*)} can be obtained using the iterative Eq. (26):

*φm*<sup>+</sup>1(*x*) = *λ* ∫ *<sup>b</sup> a k*(*x, t*)*φm*(*t*)*dt* + *f*(*x*) (26)

if *lim m*→∞*φm*(*x*) exists, the limit function is the exact solution of the equation.

#### *2.2. Numerical methods*

The numerical methods for phase change heat transfer consist of the frontier tracking method, fixed frontier method, and fixed region method according to different processing methods of the moving interface [\[72\]](#page-25-0). The frontier tracking method and the fixed frontier method require tracking of the interface position while the fixed region method does not need to.

## *2.2.1. Frontier tracking method*

The frontier tracking method firstly directly discretizes the original control equations and the boundary conditions, and then continuously tracks the position of the phase change moving interface during the solving process [[73\]](#page-25-0). It can achieve the solution with high accuracy, but its calculation amount is relatively large and the operation is relatively complex. Therefore, it is mainly used to solve one-dimensional phase transition applications and does not apply to non-isothermal phase transitions or phase transition problems with complex interface shapes [[74\]](#page-25-0).

The frontier tracking method includes the fixed step method and the variable time step method. Among them, the fixed step method [\[75](#page-25-0)] refers to that the space step and time step remain unchanged in the whole calculation process. Accordingly, because of the fixed time and space, the fixed step method accompanies some deviation in solving the changing phase transition problem.

## *2.2.2. Fixed front method*

The fixed front method was first proposed by Crank [\[76](#page-25-0)] to solve phase change problems. The core idea is to change the moving frontier to a fixed frontier by appropriate variable transformation. After that, the moving region problem can be solved as a fixed region problem. This method includes the hot surface movement method and the independent variable transformation method. It is mainly applicable to the one-dimensional case and is quite complicated for the two- and three-dimensional solutions. Mitchell et al. [[77\]](#page-25-0) compared the fixed front method and heat balance integral method in solving the phase transition problem of a one-dimensional plate swept by supercooled liquid.

The independent variable transformation method proposed by Landan et al. [[78\]](#page-25-0) is also identified as the moving boundary fixing method. It transforms the moving boundary into a fixed boundary through the transformation of spatial variables. However, in the process of independent variable transformation, the governing equations have to be transformed into nonlinear equations, which results in the first derivative term appearing in the solution and therefore bringing difficulty to the solution and limits the application of the independent variable transformation method.

#### *2.2.3. Fixed grid method*

The fixed grid method [\[79](#page-25-0)] is to build a unified energy equation within the whole solution region and then transform the heat conduction problem solved by the partition to the nonlinear heat conduction problem in the whole region without tracking the position of the two-phase interface.

The fixed grid method is the most popular numerical method for solving phase transition problems. It is greatly recommended because it completes the solution of the phase change process with high flexibility and is suitable for multi-dimensional and multi-interface situations. The fixed grid method includes the enthalpy method, the sensible heat capacity method, and the equivalent heat capacity method.

*2.2.3.1. Enthalpy method.* The enthalpy method was first proposed by Voller et al. [\[80](#page-25-0)] in 1987. Its core idea is to apply enthalpy and temperature to describe the law of conservation of energy and couple the influence of latent heat in the definition of enthalpy [[81\]](#page-25-0).

The enthalpy method simultaneously takes enthalpy and temperature as the functions to be solved, so the method first establishes a unified energy equation over the entire domain of the heat transfer process, and then the enthalpy distribution can be determined by numerical calculation method and hence the two-phase interface can be determined. Therefore, the enthalpy method not needs to track the phase interface, which is suitable for multi-dimensional cases and has been widely used in various phase change heat transfer problems.

The most commonly used integral form equation of the enthalpy method is [\[82](#page-25-0)]:

*d dt*∫ *v ρhdV* + *s ρhv*⋅*dA* = *s κ*∇*T*⋅*dA* + *v qdV* ˙ (27)

The link between enthalpy and temperature can be described as follows when the specific heats of the liquid and solid phases, respectively, are constant:

*T* − *Tm* = ⎧ ⎪⎪⎨ ⎪⎪⎩ *h* − *h*<sup>∗</sup> *s* )/*cp,<sup>s</sup> <sup>h</sup> <sup>&</sup>lt; <sup>h</sup>*<sup>∗</sup> *s* 0 *h*<sup>∗</sup> *<sup>s</sup>* ≤ *h* ≤ *h*<sup>∗</sup> *<sup>l</sup>* ( *h* − *h*<sup>∗</sup> *l* )/*cp,<sup>l</sup> <sup>h</sup> <sup>&</sup>gt; <sup>h</sup>*<sup>∗</sup> *l* (28)

Zhang et al. [\[83](#page-25-0)] developed a mathematical model for the two-dimensional enthalpy method and conducted validation experiments on a hollow block wall equipped with PCM at different periodic temperatures. Biswas et al. [\[84](#page-25-0)] developed a two-dimensional model for a wall panel with nanometer PCM based on the enthalpy method. Kuboth et al. [\[85](#page-25-0)] used the enthalpy method to establish a mathematical model and analyze the effects of the distribution of different annular fins on the exothermic performance of the thermal storage module. Bas¸al et al. [[86](#page-25-0)] carried out numerical research on a three-tube heat exchanger by enthalpy method. The results revealed that the three-pipe type was more sensitive to the mass flow rate. dos Santos et al. [\[87](#page-25-0)] used the enthalpy method to reveal the phase change heat transfer process around the horizontal finned tube. Gorzin et al. [\[88](#page-25-0)] studied the melting process of RT-50 using the enthalpy method. Ding Z et al. [\[89](#page-25-0)] build a three-dimensional model for a quarter-cell square copper column array containing water composite PCM and applied the enthalpy method to investigate the effect of copper-enhanced heat transfer on the phase transition process. Loem et al. [\[90](#page-25-0)] introduced RT-18HC with a melting point of 18 ◦C to lower the power consumption of an inverter air conditioner and predicted the phase change temperature by the enthalpy method model. EI Mohamed et al. [[91\]](#page-25-0) applied the enthalpy method to find the most effective wall structure for multi-stored residential walls. Merlin K et al. [\[92](#page-25-0)] built a numerical model by the enthalpy method to reveal the heat transfer pattern inside the PCM. Jin et al. [[93\]](#page-25-0) found that when the PCM state changed during the step-size calculation, the model created by the enthalpy method had no calculation error while the model created by the equivalent heat capacity method had a calculation error.

However, the application of the enthalpy method is strictly restricted because it needs to solve both the enthalpy and temperature at the same time and the calculation process is complicated. Most important of all, the variations of enthalpy value with the temperature of most materials are seriously lacking in practical applications.

*2.2.3.2. Sensible heat capacity method.* The sensible heat capacity method introduces the concept of equivalent specific heat capacity, regards the latent heat of phase change as a large heat capacity in the phase change temperature range, transforms the phase change problem of two phases into a single-phase nonlinear heat conduction problem,

and finally obtains the temperature field distribution and determines the position of the phase change interface [[94,95](#page-25-0)]. This method is simple and practical and is suitable for fixed PCMs with low fluidity or phase change heat transfer problems occurring within a certain temperature range.

Based on the hypothesis of this method, the piecewise function for the sensible heat capacity could be expressed as follows:

*cp,eff* = ⎧ ⎨ ⎩ *cp,<sup>s</sup> T < Ts* ( *cp,<sup>s</sup>* + *cp,<sup>l</sup>* )/<sup>2</sup> <sup>+</sup> *<sup>L</sup>/*(*Tl* <sup>−</sup> *Ts*) *Ts* <sup>≤</sup> *<sup>T</sup>* <sup>≤</sup> *Tl cp,<sup>l</sup> T > Tl* (29)

Alawadhi [\[96](#page-25-0)] explored the phase transition process of pure water in a circular shell by the sensible heat capacity method. Alawadhi et al. [[94\]](#page-25-0) simulated the solidification process taking place in the closed space of a horizontal ellipse based on the sensible heat capacity method. Han et al. [\[97](#page-25-0)] revealed the influence of the multi-cavity structure of phase change microcapsules on heat storage and release capacities based on the sensible heat capacity method. Borderon J et al. [\[98](#page-25-0)] optimized the melting temperature range of PCM with drawing support from the sensible heat capacity model. Artinov et al. [\[99](#page-25-0)] revealed the effect of latent heat on the temperature field with the help of the sensible heat capacity method. Khattari et al. [\[100\]](#page-25-0) drew support from the sensible heat capacity method to analyze the operating pattern in building materials with micro-encapsulated PCM. Bouhal T et al. [\[101\]](#page-25-0) simulated the phase change phenomenon within a solar water storage tank; the advantages of the sensible heat capacity method and the enthalpy method for numerical calculation were compared. Rabin et al. [[102](#page-26-0)] compared the sensible heat capacity method with the finite element method in dealing with multidimensional heat transfer problems; the results showed that the calculation accuracy of the sensible heat capacity method was satisfactory, and it had obvious advantages in dealing with multidimensional problems.

However, it is easy to miss the phase transition temperature range when the temperature range is small, which is a significant disadvantage of the sensible heat capacity method.

*2.2.3.3. Equivalent heat capacity method.* The equivalent heat capacity method is also known as the additional specific heat capacity method and it is an improvement on the sensible heat capacity method. The principle is to convert the latent heat of phase change released or absorbed in the process of phase change into the additional heat capacity from solidus temperature to liquidus temperature, which is added to the real specific heat capacity of the material. Therefore, the improved definition of the equivalent specific heat capacity consists of two parts: the inherent specific heat capacity and the additional specific heat capacity from the latent heat [\[103\]](#page-26-0).

The equivalent specific heat capacity can be expressed as:

*cp,eq* = *cp,<sup>i</sup>* + *L /* (*Tl* − *Ts*) (30)

Based on the equivalent heat capacity method, the phase-change process can be equated to an expansion in specific heat capacity and further can be thermodynamically analyzed [[104](#page-26-0)]. Comparatively speaking, this method can be easily implemented and is applicable to solve phase change problems with non-pure substances.

Zhang [[105\]](#page-26-0) improved the two-dimensional equivalent heat capacity model and applied it to predict the transient heat transfer process of a building envelope integrated PCM. Bottarelli et al. [[106](#page-26-0)] analyzed the heat transfer performance of adding PCM into the backfill material of ground heat exchangers based on the equivalent heat capacity method. Li et al. [[107](#page-26-0)] applied the equivalent heat capacity method to numerically analyze cryosurgery surgery. Purlis et al. [\[108\]](#page-26-0) relied on the equivalent heat capacity method to research the bread-baking process numerically. Jin et al. [\[93](#page-25-0)] compared the PCM heat transfer models which were respectively established by the enthalpy method and the equivalent heat capacity method. They found that the calculation time of the equivalent heat capacity method is shorter than that of the enthalpy method when the time step changes.

However, the application of the equivalent heat capacity method faces several constraints. Firstly, there may be an unreasonable increase in latent heat, which may lead to the wrong outcome. Particularly, the wrong outcome is difficult to find and correct. Secondly, the transition of latent heat will inevitably lead to the equivalent specific heat capacity with a big value, which leads to convergence difficulty in numerical calculation.

To sum up, each method has its own strengths and shortcomings. [Table 2](#page-10-0) summarizes the practical applications of the fixed grid method.

## *2.3. CFD numerical methods*

CFD numerical methods [\[109\]](#page-26-0) are fluid mechanics analysis methods based on computer simulation, which can simulate the movement and change of fluid under different conditions. The basic idea is that the original values of physical quantities, such as speed and temperature in time and space, are replaced by the values of finite discrete points (nodes). The algebraic equations of the relationship between the variables of each node are established by energy equation, continuity equation, and momentum equation, to obtain the approximate values of the required physical parameters at each node. The nodes are divided densely enough with the continuous development of computer technology to ensure the accuracy of the results, which makes CFD numerical methods more accurate and reliable in engineering design and scientific research. At present, the widely used CFD numerical methods include the finite volume method, finite element method, finite difference method, finite analytic method, lattice Boltzmann method, and particle method.

## *2.3.1. Finite volume method*

The finite volume method [\[109\]](#page-26-0) divides the calculation area into a series of control volumes, each node represents a control volume, and the discrete equations are derived by using a certain number of control equations for the control volume. The discrete equations derived by the finite volume method still have conservation properties and the discrete equation coefficients have exact physical meaning. Aiming at the phase change process, the finite volume method can lift the calculation speed without increasing the error, so it has become the most commonly used numerical solution method. The FLUENT software uses the finite volume method as its computational kernel. Gracia et al. [[110](#page-26-0)] applied the finite volume method to optimize the distribution of phase change units in a thermal storage water tank.

# *2.3.2. Finite element method*

Comini et al. [\[111\]](#page-26-0) first used the finite element method to solve the phase change process. The finite element method divides the calculation area into a series of unit body, and takes several points as nodes on each unit bodies and then the discrete equation is obtained by integrating the governing equations. Although the finite element method is well adapted to irregular regions, its computational volume is generally large, and some treatment methods in solving flow and heat transfer problems are not as mature as the finite volume method. Sarkar et al. [[112](#page-26-0)] applied the finite element method to study the melting process of PCMs in rectangular structures.

#### *2.3.3. Finite difference method*

The finite difference method replaces the target solution region with a collection of points formed by the intersection of a series of grid lines parallel to the coordinate axes. At each discrete point, each derivative in the corresponding governing equation is replaced by the difference expression, so an algebraic equation can be formed at each discrete point. By solving these equations, numerical solutions can be obtained. However, this method shows poor adaptability to complex regions and is difficult to ensure the conservation of numerical solutions. Liu et al.

<span id="page-10-0"></span>**Table 2**  Applications of the fixed grid method.

**Table 2** (*continued* )

[[113](#page-26-0)] studied the thermal properties of a double-glazed roof filled with PCMs by the finite difference method.

#### *2.3.4. Finite analytic method*

The finite analysis method [[114](#page-26-0)], like the finite difference method, discretizes the solution region with a series of grid lines, but the difference is that each node of this method forms a calculation unit with four adjacent grids. Then, through a series of calculations and analyses, the algebraic equations of unknown variables at all points in the unit can be obtained. The node division of the these four types of CFD numerical methods is shown in Fig. 4.

#### *2.3.5. Lattice Boltzmann method*

Lattice Boltzmann method (LBM) [\[115\]](#page-26-0) is a new numerical CFD

**Fig. 4.** Node division of different CFD numerical methods.

method that has emerged in recent decades. This method does not solve the Navier-Stokes equation under the way of the traditional CFD numerical methods but simulates the motion behavior of the whole fluid by calculating the two processes of streaming and collision between microscopic particles. The lattice model in LBM was proposed by Qian et al. [[116](#page-26-0)] in 1992. This model is also called the DdQm model, that is, the model of *d* dimensional space and *m* discrete velocities. Fig. 5 shows the schematic diagram of a common two-dimensional typical lattice model.

The general equation of LBM is as followed:

*fi*(*x* + *ei*Δ*t, t* + Δ*t*)− *fi*(*x, t*) = [*fi*(*x, t*)− *f eq <sup>i</sup>* (*x, t*)] */ τ* (31)

Based on the solution characteristics of streaming and collision, LBM shows advantages in computational simplicity, high parallel efficiency, and easy boundary processing.

Tao et al. [[117](#page-26-0)] studied the effect of pore density and porosity on the latent heat storage of copper composite PCM by LBM. Huo et al. [[118](#page-26-0)] innovatively studied the phase transition process of PCM in spherical capsules by LBM.

#### *2.3.6. Particle method*

The particle method is a meshless method based on the lagrangian. The basic idea is to discretize the fluid in the computational domain into a series of particles with material properties, velocity, and pressure; and the motion of the particles follows the conservation equations of momentum, mass, and energy. The governing equation is discretized by the interaction model between particles, and the position and physical information of each particle are solved to obtain the behavior of the whole solution domain. The characteristic of this method is that there is no numerical dissipation problem of the convection term, and it is much more convenient than the grid methods when dealing with complex boundaries. Commonly used particle methods include the smoothed particle hydrodynamics method [[119](#page-26-0)], the moving particle semi-implicit method [\[120\]](#page-26-0), and the finite volume particle method [[121](#page-26-0)].

Characteristics of different methods are listed in [Table 3](#page-13-0) in detail.

#### **3. Numerical simulation method by CFD**

## *3.1. Introduction of the CFD software and common solution methods*

Computational fluid dynamics (CFD) software is powerful tools to deal with the non-linearizability problems of momentum, heat, and mass transfer processes [\[122\]](#page-26-0). For the multi-dimensional or complex boundary phase change heat transfer problems, numerical simulation can reveal the details of the heat transfer process in more concrete.

FLUENT is an efficient software for computational fluid dynamics and heat transfer problems. It is popular in laminar and turbulent flow, multiphase flow, heat transfer, and phase change, porous media, chemical reaction and combustion, rotating machinery, and so on. In recent years, in addition to FLUENT, some other software has also been used for numerical simulations, such as COMSOL, CFX, and so on. Each of them has its characteristics, such as COMSOL providing a powerful multi-physical field coupling function. CFX has computational advantages in multiphase flow, phase change mass transfer, and boiling heat transfer. OpenFOAM which is normally served as a CFD open-source program package presents advantages in stable operation, efficient parallel computing ability, and advanced solution method. They used the these software to simulate research PCM as follows: Ferfera et al. [[123](#page-26-0)] numerically studied the heat storage performance of heat exchangers with PCM embedded in metal foam by COMSOL software. Aziz et al. [[124](#page-26-0)] used CFX software to simulate the charge and discharge performances of a sphere-encapsulated PCM. Kasibhatla et al. [[125](#page-26-0)] established a numerical model to precisely simulate the melting process of PCM-filled capsules by using OpenFOAM software.

FLUENT has outstanding advantages, such as comprehensive functions, low cost, high efficiency, fast, and convenience, most research works tend to use FLUENT to simulate the phase change process of PCMs [[126](#page-26-0)].

There are several common solutions in FLUENT. The SIMPLE algorithm is used to solve the coupling problem of velocity and pressure in the momentum equation, which is also the default algorithm in FLUENT. It has good stability and is mainly used to solve incompressible flow fields [\[127\]](#page-26-0). The discrete schemes for the convection term include first-order upwind scheme, second-order upwind scheme, QUICK scheme, and so on. The first-order upwind scheme has a better convergence speed but poor convergence accuracy; besides, it accompanies by a serious false diffusion when the *Pe* number (Peclet number) is large. The second-order upwind scheme shows relatively good computational accuracy for complex flows, but its convergence speed is slow and still exists the false diffusion problem. QUICK scheme [\[128\]](#page-26-0) can reduce the false diffusion and achieve the calculated results with high accuracy. It is considered one of the reliable difference schemes [\[129\]](#page-26-0). However, the calculation speed of the QUICK scheme is also slow and the stability is inferior to the second-order upwind scheme. PRESTO scheme which belongs to the pressure interpolation method is usually used to discrete pressure. It is more effective in solving problems with large vortex numbers and high-speed rotating flow.

**Fig. 5.** Two-dimensional typical lattice model.

<span id="page-13-0"></span>**Table 3**  Characteristics of different solution methods.

# *3.2. Solidification and melting model in FLUENT*

#### *3.2.1. Introduction of solidification and melting model*

The solidification and melting model adopted by FLUENT is based on the enthalpy-porosity method proposed by Voller and Prakash [[80\]](#page-25-0) in 1987. In this method, the liquid phase ratio is introduced to describe the change process of the solid-liquid interface indirectly and the two-phase coexistence region of PCMs is treated as the flow field, which avoids tracking the interface position of phase transition and simplifies the calculation process. As shown in [Fig. 6](#page-14-0), the PCMs region can be divided into a fluid region, a solid region, and a two-phase mushy region. The governing equation is as follows [\[130\]](#page-26-0):

The continuity equation:

<sup>∂</sup>*<sup>ρ</sup> /* <sup>∂</sup>*<sup>t</sup>* <sup>+</sup> <sup>∇</sup> <sup>⋅</sup>(*ρ*→*<sup>ν</sup>* ) <sup>=</sup> <sup>0</sup> (32)

Momentum equations:

<sup>∂</sup>(*ρ*→*<sup>v</sup>* ) */* <sup>∂</sup>*<sup>t</sup>* <sup>+</sup> <sup>∇</sup> <sup>⋅</sup>(*ρ*→*<sup>v</sup>* <sup>→</sup>*<sup>v</sup>* ) <sup>=</sup> <sup>−</sup> <sup>∇</sup>*<sup>P</sup>* <sup>+</sup> <sup>∇</sup> <sup>⋅</sup>(*μ*∇→*<sup>v</sup>* ) <sup>+</sup> *ρg* <sup>+</sup> *<sup>S</sup>* (33)

*<sup>S</sup>* <sup>=</sup> *Amush*→*<sup>v</sup>* (<sup>1</sup> <sup>−</sup> *<sup>β</sup>*) <sup>2</sup> / ( *β*<sup>3</sup> + *ε* ) (34)

Energy equation:

<sup>∂</sup>(*ρH*) */* <sup>∂</sup>*<sup>t</sup>* <sup>+</sup> <sup>∇</sup> <sup>⋅</sup>(*ρ*→*<sup>v</sup> <sup>H</sup>*) <sup>=</sup> <sup>∇</sup>⋅(*κ*∇*T*) (35)

*H* = *h* + Δ*H* (36)

*h* = *href* + ∫ *<sup>T</sup> Tref cp,pdT* (37)

Δ*H* = *βL* (38)

*β* = ⎧ ⎨ ⎩ 0 *T < Ts* (*T* − *Ts*)*/*(*Tl* − *Ts*) *Ts < T < Tl* 1 *T > Tl* (39)

The mushy region is a semi-solid region that exists as the interface between the melted region and the unmelted region of the PCMs [[131](#page-26-0)]. *Amush* is used to indicate the amount of change in the velocity of the material as it solidifies [[132](#page-26-0)]. The larger the *Amush*, the faster the velocity decreases as the material solidifies. It has been determined that the value of *Amush* shows an important influence on the accuracy and correctness

<span id="page-14-0"></span>**Fig. 6.** Phase transition temperature interval model.

**Table 4**  The suggested values of *Amush* for different PCMs.

of the heat transfer performance during solidification and melting [\[133](#page-26-0), [134](#page-26-0)]. Therefore, it is very important to select the reasonably mushy constant to simulate the solidification and melting processes of PCM. Some of the suggested *Amush* values used for different PCMs and different geometries have been summarized in Table 4 for reference.

#### *3.2.2. Applications of solidification and melting model*

The solidification and melting model in FLUENT are often used to simulate the phase transition process of PCMs. They found that the aims of increasing the solidification/melting rate and shortening the phase change time could be realized by improving the performance of a heat storage unit and accelerating the heat transfer during the phase change process.

Hosseini et al. [\[143\]](#page-26-0) applied FLUENT to simulate the melting and solidification processes of paraffin RT50 in shell and tube heat exchangers. The results indicated that when the inlet temperature of heat transfer fluid (HTF) raised from 70 ◦C to 80 ◦C, the theoretical efficiencies in melting and solidification processes respectively increased to 88.4% and 81.4%, and the melting time shortened by 37%. Abdulrahman et al. [[144](#page-26-0)] applied FLUENT to analyze the melting process within a rectangular heat exchanger filled with PCM. Their results revealed that increasing the Reynolds number at the hot fluid side can promote the heat transfer rate and accelerate the melting process of PCM. Yadav et al. [[145](#page-26-0)] simulated the melting process of paraffin and obtained the variation rule of paraffin controlled by heat conduction and heat convection. Li et al. [[146](#page-26-0)] explored the influences of volume flow rate and inlet temperature of HTF on the melting rate of PCM by FLUENT. The results indicated that by increasing the volume flow rate from 0.503 m<sup>3</sup> /h to 0.936 m<sup>3</sup> /h, the volume fraction of molten PCM can be lifted from 63.33% to 70.74% within 600 s; the higher the inlet temperature of HTF, the higher the melting rate of PCM.

Many studies have pointed out that changing the geometrical structure of the device, introducing composite PCMs, and arranging different shapes of fins can increase the rate of phase change heat transfer. Ehms et al. [\[130\]](#page-26-0) revealed that the effect of the diameter of the spherical unit was greater than the temperature difference between the wall temperature and the PCM during the solidification process. Li et al. [[147](#page-26-0)] presented the melting process of paraffin within a spherical unit immersed in a flume by FLUENT. The results indicated that the smaller the radius of the sphere, the quicker the melting rate of the PCM. Zheng et al. [\[148\]](#page-26-0) conducted a simulation on the melting processes of copper foam and paraffin composite PCM by FLUENT and found that introducing the metal foam can shorten the melting time of paraffin by 20.5%. Al-Abidi et al. [\[149\]](#page-26-0) arranged inner and outer fins within a three-tube heat exchanger (TTHX) to enhance heat transfer. The results simulated and analyzed by FLUENT revealed that the fin length and fin number presented great influence on the melting speed of PCM and the total melting time under the optimized arrangement can be reduced by 34.7%. Al-Abidi et al. [\[150](#page-26-0)] also further explored the solidification process by using the same method. They pointed out that compared with other schemes, the time of complete solidification under the optimized arrangement can be shortened by 35% when the fin thickness was 1 mm. Yang et al. [[151](#page-26-0)] simulated the PCM melting process of a shell-and-tube latent heat thermal energy storage(LHTES)device with annular fins. The results showed that the melting time can be reduced 65% by arranging annular fins into PCM. Zhang et al. [[152](#page-26-0)] proposed a novel fractal tree-shaped fin and applied it to promote the overall performance of a shell and tube heat storage device. Their results based on numerical simulation found that the fractal tree fins can significantly improve the heat charge and heat discharge rates of the unit and shorten the melting time and solidification time by 4.4% and 66.2%, respectively.

In practical applications, this model will also be used to simulate the phase transition process. Kheradmand et al. [[153](#page-26-0)] applied FLUENT to reveal the influence of plastering mortar with PCM mixture on the operating pattern of buildings. They found that compared with ordinary mortar or mortar with a single type of PCM, plastering mortar with a mixed PCM mixture can significantly lower the temperature requirement of heating/cooling and effectively improve the energy efficiency of buildings. Zhong et al. [[154](#page-26-0)] explored the influences of thermophysical parameters on the transient heat transfer performance of a glass window filled with PCM (PCMW) and found that reducing the temperature difference between the solid phase and liquid phase could improve the thermal performance of PCMW; the optimum melting temperature ranged between 25 ◦C–31 ◦C. Gowreesunker et al. [\[155\]](#page-26-0) filled PCM into double glazing and investigated its performance experimentally and numerically. Experimental results and FLUENT simulations concluded that the latent heat of PCM can significantly determine the thermal properties of double glazing.

However, in recent years, studies have also proven that PCMs in double-glazed windows releases a lot of heat into the room during summer nights; moreover, the overheating phenomenon caused by the completely melted PCMs cannot be ignored. Therefore, Li et al. [[156](#page-26-0)] proposed a triple-layer glass filled with PCM to overcome the these problems and investigated its thermal performance in winter and summer by numerical simulation with FLUENT. The results revealed that the proposed glass can save energy consumption up to 32.8% and effectively prevent overheating in summer; meanwhile, the thermal insulation effect was significant in winter.

To sum up, the model approach, types of PCMs, main research content, and the major conclusion are summarized in [Table 5](#page-15-0) in detail.

<span id="page-15-0"></span>**Table 5**  Applications of solidification and melting model.

**Table 5** (*continued* )

**Table 5** (*continued* )

#### *3.3. Integrating natural convection with simulation method in FLUENT*

#### *3.3.1. Models of natural convection in FLUENT*

Under the influence of gravity, the inhomogeneity of the temperature field causes inhomogeneity in density and thus generates buoyancy force, and leads to natural convection occurring in the liquid zone of the PCM.

Generally, the density of the liquid phase away from the heating wall is assumed as *ρl,*1 while the density of the liquid phase near the heating wall is *ρl,*0, then:

*ρl,*<sup>0</sup> = *ρl,*1(1 − *β*Δ*T*) (40)

The pressure difference formed at these two points is Δ*p*, which is defined as:

<sup>Δ</sup>*<sup>p</sup>* <sup>=</sup> *ρl,*1*gl* <sup>−</sup> *ρl,*0*gl* <sup>=</sup> *ρl,*0*glβ*Δ*<sup>T</sup>* / (1 − *β*Δ*T*) (41)

When Δ*t* is relatively small, there are:

Δ*p/ρl,*<sup>0</sup> ≈ *glβ*Δ*T* (42)

Due to the existence of pressure difference, the flow in the liquid phase is bound to generate flow velocity. The relationship between the pressure difference and the velocity is as followed:

*u*2 / 2 ) ∝( Δ*p* / *ρl,*<sup>0</sup> ) ≈ *glβ*Δ*T* (43)

That is:

*<sup>u</sup>*<sup>∝</sup> ̅̅̅̅̅̅̅̅̅̅̅̅̅ *glβ*Δ*<sup>T</sup>* <sup>√</sup> (44)

where, Δ*T* is the temperature difference between two points, k. *l* is the height of the heating surface, m.

Through the analysis, it can be seen that the flow velocity is related to the nature, flow space, and geometry of the fluid.

The natural convection makes the temperature field and velocity field exist at the same time, and their interaction determines the geometric shape of the solid-liquid phase interface, which makes the solution of the phase change heat transfer process more complicated. Therefore, FLUENT can be used to simulate the phase change process, which can better understand its heat transfer mechanism and restore the actual phase change process.

## *3.3.2. Applications of natural convection based method*

In the actual phase transformation processes, natural convection caused by temperature difference always exists and its influence turns to non-negligible as the proportion of the liquid phase increases. Thus, it is important to take the influence of natural convection on the actual phase change process into account when conducting numerical simulations. Generally, when the FLUENT software is used for simulation, the solidification and melting model can be selected, the Gravity term can be activated with the direction of the negative direction of *Y*, and the Boussinesq hypothesis is additionally set to approximate the influence of natural convection.

Previous studies have proven that natural convection plays an important role during the PCM melting process and can accelerate the melting rate [\[157\]](#page-26-0). However, heat conduction is the main heat transfer way during the solidification of PCM [[158](#page-26-0)].

Seddegh et al. [[159](#page-26-0)] applied FLUENT to reveal the influence of natural convection on the solidification/melting process of PCM within a vertical shell and tube energy storage system. Their results concluded that natural convection was decisive in the melting process; it can significantly enhance heat transfer. Fornarelli et al. [\[160\]](#page-26-0) simulated the melting process of PCM in a shell-and-tube heat storage device The results pointed out that *Amush* will delay the convection during heat storage, its existence cannot be ignored. Hosseini et al. [\[161\]](#page-26-0) simulated and analyzed the melting process in a shell and tube heat exchanger filled with paraffin wax and found that the temperature increased fastest above the pipe at an angle of 0◦ under the action of natural convection. Yang et al. [\[162\]](#page-26-0) simulated the melting process of PCM immersed in open-cell foam metal by FLUENT. The results showed clearly that the natural convection resulted in a 45.5% reduction in melting time. Some other studies also demonstrate that natural convection has a little impact during the solidification process and that heat conduction is the main heat transfer way [\[163](#page-26-0)–165].

From the results of these studies, it can be concluded that natural convection aggravates the inhomogeneity of PCM, especially in the melting process. Therefore, eccentric arrangement and fins are introduced to promote the heat transfer process. Eslamnezhad, H et al. [[166](#page-27-0)] numerically simulated the melting process in a three-tube heat exchanger with rectangular fins, and natural convection was considered. Based on the simulation, the optimal model was obtained. They found that arranging rectangular fins can improve the efficiency of the heat exchanger and shorten the melting time by 17.9%. Pahamli et al. [[140](#page-26-0)] stated the influence of eccentric arrangement on the melting process of a shell and tube heat exchanger. Their results pointed out that the eccentric arrangement can strengthen the natural convection and the melting time can be shortened by approximately 67% as the eccentricity was set to 0.75. Darzi et al. [[167](#page-27-0)] numerically investigated the melting processes of PCM in concentric and eccentric cases by a two-dimensional model and the results revealed that natural convection played a dominant role in determining the melting rate of PCM. Compared with the concentric case, the complete melting time of PCM in the eccentric case was significantly reduced.

Simulations of PCMs with natural convection through FLUENT are summarized in [Table 6](#page-19-0) in detail.

# *3.4. Integrating nanocomposite PCMs with simulation method in FLUENT*

# *3.4.1. Models of nanocomposite PCMs*

In 1995, Choi first proposed nanofluids at Argonne National Laboratory in the United States, in which metallic (or non-metallic) nanoscale powders were added to a common base fluid to form a new heat transfer medium with higher thermal conductivity. Compared with the early research that added millimeter and micron-sized particles, applying the nanoscale-size particles is free of pipe clogging problems and can promote the miniaturization of various heat exchange equipment [\[168\]](#page-27-0).

[Fig. 7](#page-20-0) sums up the classifications of nanomaterials. Organic nanomaterials consist of graphite, fullerenes, carbon nanotubes (CNT), nanofibers, single-walled carbon nanotubes (SWCNT), multi-walled carbon nanotubes (MWCNT); while inorganic nanomaterials include metals and metal oxide based nanomaterials such as aluminum, zinc, copper, iron, alumina, iron oxide, etc [\[169\]](#page-27-0).

Nanomaterials present advantages in nano size effect, high thermal conductivity, large specific surface effect, and strong interfacial interaction. Khodadadi and Hosseinizadeh [\[170\]](#page-27-0) proposed at an early stage that dispersing nanoparticles into PCMs to form nanocomposite PCMs (NPCMs) can improve their heat transfer performance and ameliorate the drawback of the low thermal conductivity of PCMs. It is worth noting that NPCMs and nano-enhanced PCMs (NEPCMs) [[171](#page-27-0),[172\]](#page-27-0) both improve the properties of PCMs by adding nanoparticles, and they are both used in many studies.

The thermophysical properties of NPCMs are listed as follows:

*ρnf* = (1 − *φ*)*ρf* + *φρs* (45)

*ρcp* ) *nf* = (1 − *φ*) *ρcp* ) *<sup>f</sup>* + *φ ρcp* ) *<sup>s</sup>* (46)

*μnf* = *μf* / (1 − *φ*) <sup>2</sup>*.*<sup>5</sup> (47)

(*ρβ*)*nf* = (1 − *φ*)(*ρβ*)*<sup>f</sup>* + *φ*(*ρβ*)*<sup>s</sup>* (48)

<span id="page-19-0"></span>**Table 6**  Simulations by FLUENT with natural convection.

(*continued on next page*)

#### <span id="page-20-0"></span>**Table 6** (*continued* )

**Fig. 7.** Classifications of nanomaterials.

(*ρL*)*nf* = (1 − *φ*)*ρf Lf* (49)

The effective thermal conductivity of nanofluids *κeff* can be expressed as:

*κeff* = *κnf* <sup>0</sup> + *κd* (50)

*κnf* <sup>0</sup> / *κf* <sup>=</sup> [ *κs* + 2*κf* − 2*φ κf* − *κs* )] / [ *κs* + 2*κf* + *φ κf* − *κs* )] (51)

Enhancement of thermal conductivity due to thermal diffusion *κd*is:

*κd* = *D ρcp* ) *nf* <sup>+</sup> ̅̅̅̅̅̅̅̅̅̅̅̅̅̅ *u*<sup>2</sup> + *v*<sup>2</sup> √ *φdp* (52)

# *3.4.2. Applications of nanocomposite PCMs based method*

With the development of nanomaterial technology, introducing high thermal conductivity metal nanoparticles, graphene nanosheets, and other nanoscale materials to enhance the heat storage and heat release rates of PCMs has become a research hotspot [[46,](#page-25-0)[169](#page-27-0)].

The addition of nanoparticles could shorten the melting time of composite PCMs. Meanwhile, the nanoparticles play the role of condensation nucleus in the solidification process, which reduced the undercooling degree of PCMs. However, it should be noted that adding nanoparticles with higher volume fraction will simultaneously lead to agglomeration and settlement, which deteriorates the stability of composite PCMs. The solidification and melting model in FLUENT can be used to simulate the phase transition process of NPCMs.

Kashani et al. [[173](#page-27-0)] applied FLUENT to simulate the melting process in rectangular and cylindrical vessels filled with nanocomposite PCMs. Their results demonstrated the dispersion of nanoparticles enhanced the thermal conductivity of the PCM by 30%, lifted the heat transfer rate by 15%, and thus shortened the melting time by 15%. Hosseinizadeh et al. [[174](#page-27-0)] presented the melting process of nanocomposite PCMs in a spherical container and proved that compared with conventional PCM, the addition of nanoparticles enhanced its thermal conductivity. Sebti et al. [[141](#page-26-0)] simulated the enhanced heat transfer process with paraffin-based nanofluids containing different volume fractions of copper in a two-dimensional square cavity and found that increasing the volume fraction of nanoparticles can enhance the heat transfer rates of nanofluids. Arıcı et al. [\[175\]](#page-27-0) simulated the influence of the volume fraction of Al2O3 nanoparticles on the melting rate of a square container filled with paraffin and found that the melting rate of paraffin took the maximum value when the volume fraction was 1%. Dhaidan et al. [[176](#page-27-0)] applied FLUENT to simulate the melting process of n-octadecane doped with CuO nanoparticles in a horizontal circular container. The results demonstrated that adding a higher concentration of nanoparticles may cause agglomeration and precipitation of particles. Kashani et al. [[177](#page-27-0)] displayed the solidification process of nano-copper and water composite PCM in a vertical wave-wall cavity by numerical simulation and found that the dispersion of nano-particles in the PCM enhanced the solidification rate. Besides, increasing the waviness will also lead to an increase in the total solidification time. Valan et al. [\[178\]](#page-27-0) simulated the heat transfer patterns during melting and solidification processes within a shell and tube heat exchanger filled with paraffin and alumina nanocomposite PCM. Their results revealed that compared with pure paraffin, the solidification rate increased by 33.3% while the melting rate increased by 3.5% when the content of nanoparticles was 10%.

The simulation studies of the NPCMs based on FLUENT are summarized in [Table 7](#page-22-0) in detail for reference.

### **4. 4. Summary**

In this study, the principle, advantages, disadvantages, and applicable situations of the methods for solving the phase change processes are summarized, including analytic methods, numerical methods, and CFD numerical methods. Then, the CFD software for simulating the phase change processes and the solidification and melting model in FLUENT are introduced. The numerical simulation studies of the phase

transition process, especially the influence of natural convection and nanoparticles on the solidification/melting processes, are summarized and discussed. Moreover, the simulation methods used, the PCMs used, and the devices used in this study are summarized in detail.

#### *4.1. Conclusions*

- 1) The many advantages of PCMs make them play an important role in the field of energy saving and environmental protection and have a broad application prospect in the fields of construction engineering, solar energy, industrial waste heat utilization and so on.
- 2) Due to the complexity of phase change problems, specific solution methods are required to obtain the solutions for different phase change models during the solution process. The enthalpy method, the sensible heat capacity method, and the equivalent heat capacity method are suitable for multi-dimensional and multi-interface situations and they are used most frequently and widely in practical engineering applications.
- 3) The solidification and melting model in FLUENT is often used to simulate the phase change process of PCMs. However, this model also has its inherent limitations, that is, it can only be used with uncoupled solvers, it cannot be used for compressible fluids, and it cannot simulate phase change heat transfer about multiphase flows.
- 4) In the actual phase change processes, natural convection is crucial to the melting process of PCMs because it can speed up the melting of PCMs and improve work efficiency.
- 5) The dispersion of nanoparticles can increase the thermal conductivity of the composite PCMs, shorten the melting time of the composite PCMs, and lower the undercooling degree of the PCMs during the solidification process. It is worth noting that the appropriate nanoparticle concentration should be selected; otherwise, the phenomenon of particle settlement and agglomeration will occur.

#### *4.2. Prospects*

- 1) The applications of PCMs are limited by the problems of poor chemical stability, low thermal conductivity, easy corrosion, easy phase separation, and high cost. Future research on PCMs can focus on the development of nano-sized PCMs and multifunctional composite PCMs to replace single-performance organic/inorganic PCMs.
- 2) The encapsulation technologies of PCMs are particularly important to improve the utilization rate of PCM. Particularly, the nanoencapsulation technology can effectively solve the problem of PCMs encapsulation in smaller scale. However, more efforts should be paid on developing the processes with easy operation, broad adoption, strong sealing, low cost, and long life.
- 3) At present, most of the research focuses on the application of PCMs in numerical simulation and small-scale experiments. In the future, it is necessary to improve the durability, applicability, and economy of PCMs, expand reasonably the application range of PCMs, achieve low-carbon environmental protection, and make it common green energy in society.
- 4) The numerical models need to adopt the same dimensional structure as experimental devices. Therefore, the establishment of the threedimensional numerical model should be focused on in future research.
- 5) It is worth mentioning that many numerical simulations of phase change processes have not been verified by experiments. Future research should combine simulations with experiments to ensure the accuracy of model verification.
- 6) In the numerical simulations or experiments based on FLUENT, some studies ignore the special situations in the phase transformation process, such as natural convection, undercooling, precipitation, external influence, and other practical factors. The future research work should focus on fully mastering the phase transition process, using multiple groups of parameters to conduct simulation

<span id="page-22-0"></span>**Table 7** FLUENT simulations of NPCMs.

**Table 7** (*continued* )

- <span id="page-24-0"></span>experiments, and providing more effective means to simulate special conditions in the phase transition process.
- 7) The research on the influence of natural convection on the phase change process is mainly through numerical simulation, while experimental research is relatively few. The simulation results lack support from independent experimental data. In future research, more research based on visualization experiments should be developed.
- 8) To prevent a big deviation between the simulation results and the actual experimental results, actual measurements of the effective thermal properties of nanocomposite PCMs should be fully developed further to instead of theoretical predictions.

However, there are limitations in this study. Firstly, this study only introduces the governing equation, advantages, disadvantages, applicability of analytical solution methods and numerical solution methods, the description of the generalized abstraction of the object in the actual treatment as well as the introduction and treatment of the convergence of the equation in the actual solution process is missed. Secondly, Fluent is emphatically introduced as the representative of CFD software in this study, but the advantages, disadvantages, governing equations, and applicability of other CFD software and their simulation research are not introduced in detail due to the space limitation. Finally, there may be possibility that some of unusual methods are not involved due to the authors' scope limitation of knowledge.

#### **Author contributions**

T. Zhang: Conceptualization, Resources, Writing – original draft; Dongxin Huo: Resources, Data curation, Writing – review & editing; Chengyao Wang: Resources, Writing – review & editing, Supervision; Zhengrong Shi: Conceptualization, Supervision, Project administration

Detail is: For the figures in Refs. [\[47](#page-25-0)–55[,88,89](#page-25-0),[97,](#page-25-0)[106](#page-26-0),[130,140,141](#page-26-0), [143,144,](#page-26-0)146–[149,151](#page-26-0)–156[,159](#page-26-0)–162[,166,167,](#page-27-0)175–[177\]](#page-27-0), the authors have attained permissions from ELSEVIER.

#### **Declaration of competing interest**

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## **Data availability**

No data was used for the research described in the article.

#### **Acknowledgments**

The work was supported by National innovation talent promotion program (G2022013028 L), Shanghai Class IV Peak Disciplinary Development Program.

## **References**

- [1] [Wu S, Fang G, Chen Z. Discharging characteristics modeling of cool thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref1)  [energy storage system with coil pipes using n-tetradecane as phase change](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref1)  [material. Appl Therm Eng 2012;37:336](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref1)–43.
- [2] [Trp A. An experimental and numerical investigation of heat transfer during](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref2)  [technical grade paraffin melting and solidification in a shell-and-tube latent](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref2) [thermal energy storage unit. Sol Energy 2005;79:648](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref2)–60.
- [3] Wang C, Jia X, Zhao P, Wang L, Shi L. A review of the application of solid-liquid phase change materials in water heaters. Therm Sci 2023. [https://doi.org/](https://doi.org/10.2298/TSCI230311145W)  [10.2298/TSCI230311145W](https://doi.org/10.2298/TSCI230311145W). Online.
- [4] [Rashid FL, Rahbari A, Ibrahem RK, Talebizadehsardari P, Basem A, Kaood A,](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref4)  [et al. Review of solidification and melting performance of phase change materials](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref4)  [in the presence of magnetic field, rotation, tilt angle, and vibration. J Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref4) [Storage 2023;67:107501](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref4).

- [5] [Cui W, Si T, Li X, Li X, Lu L, Ma T, et al. Heat transfer enhancement of phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref5) [change materials embedded with metal foam for thermal energy storage: a](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref5) [review. Renew Sustain Energy Rev 2022;169:112912.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref5)
- [6] Niˇzeti´c S, Jurˇcevi´[c M, Arıcı M, Arasu AV, Xie G. Nano-enhanced phase change](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref6)  [materials and fluids in energy applications: a review. Renew Sustain Energy Rev](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref6)  [2020;129:109931.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref6)
- [7] [Abhat A. Low temperature latent heat thermal energy storage: heat storage](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref7) [materials. Sol Energy 1983;30:313](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref7)–32.
- [8] [Zahir MH, Mohamed SA, Saidur R, Al-Sulaiman FA. Supercooling of phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref8)[change materials and the techniques used to mitigate the phenomenon. Appl](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref8) [Energy 2019;240:793](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref8)–817.
- [9] [Peng B, Yue C, Qiu G, Wu Z, Li J. The recent research progress and application of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref9)  [phase change and energy storage materials. Mater Rev 2018;32:248](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref9)–52.
- [10] [Zhao Y, Zhang X, Hua W. Review of preparation technologies of organic](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref10)
- [composite phase change materials in energy storage. J Mol Liq 2021;336:115923.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref10) [11] [Rathod MK, Banerjee J. Thermal stability of phase change materials used in latent](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref11)  [heat energy storage systems: a review. Renew Sustain Energy Rev 2013;18:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref11) [246](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref11)–58.
- [12] [Salunkhe PB, Shembekar PS. A review on effect of phase change material](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref12)  [encapsulation on the thermal performance of a system. Renew Sustain Energy Rev](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref12)  [2012;16:5603](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref12)–16.
- [13] [Karthikeyan S, Solomon GR, Kumaresan V, Velraj R. Parametric studies on packed](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref13)  [bed storage unit filled with PCM encapsulated spherical containers for low](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref13)  [temperature solar air heating applications. Energy Convers Manag 2014;78:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref13) 74–[80.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref13)
- [14] [Liu D, Xie K, Zhang H, Qiang Y, Yang D, Wang Z, et al. Numerical evaluation of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref14)  [convective heat transfer properties of two-dimensional rotating PCM melt in the](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref14)  [unilaterally heated rectangular container. Renew Energy 2022;193:920](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref14)–40.
- [15] [Feng G, Liang D, Huang K, Wang Y. Thermal performance difference of phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref15)  [change energy storage units based on tubular macro-encapsulation. Sustain Cities](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref15)  [Soc 2019;50:101662.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref15)
- [16] [Fukahori R, Nomura T, Zhu C, Sheng N, Okinaka N, Akiyama T. Macro](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref16)[encapsulation of metallic phase change material using cylindrical-type ceramic](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref16) [containers for high-temperature thermal energy storage. Appl Energy 2016;170:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref16) [324](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref16)–8.
- [17] [Khudhair AM, Farid MM. A review on energy conservation in building](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref17)  [applications with thermal storage by latent heat using phase change materials.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref17)  [Energy Convers Manag 2004;45:263](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref17)–75.
- [18] [Hawlader M, Uddin M, Khin MM. Microencapsulated PCM thermal-energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref18) [storage system. Appl Energy 2003;74:195](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref18)–202.
- [19] [Ho C, Liu Y-C, Ghalambaz M, Yan W-M. Forced convection heat transfer of Nano-](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref19)[Encapsulated Phase Change Material \(NEPCM\) suspension in a mini-channel](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref19) [heatsink. Int J Heat Mass Tran 2020;155:119858.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref19)
- [20] [Ghalambaz M, Chamkha AJ, Wen D. Natural convective flow and heat transfer of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref20)  [nano-encapsulated phase change materials \(NEPCMs\) in a cavity. Int J Heat Mass](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref20)  [Tran 2019;138:738](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref20)–49.
- [21] [Mehryan S, Ghalambaz M, Gargari LS, Hajjar A, Sheremet M. Natural convection](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref21)  [flow of a suspension containing nano-encapsulated phase change particles in an](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref21) [eccentric annulus. J Energy Storage 2020;28:101236.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref21)
- [22] [Khan Z, Khan Z, Ghafoor A. A review of performance enhancement of PCM based](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref22)  [latent heat storage system within the context of materials, thermal stability and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref22) [compatibility. Energy Convers Manag 2016;115:132](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref22)–58.
- [23] [Umair MM, Zhang Y, Iqbal K, Zhang S, Tang B. Novel strategies and supporting](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref23) [materials applied to shape-stabilize organic phase change materials for thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref23)  energy storage–[A review. Appl Energy 2019;235:846](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref23)–73.
- [24] [Meng Z, Zhang P. Experimental and numerical investigation of a tube-in-tank](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref24)  [latent thermal energy storage unit using composite PCM. Appl Energy 2017;190:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref24)  [524](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref24)–39.
- [25] [Ma G, Liu S, Xie S, Jing Y, Zhang Q, Sun J, et al. Binary eutectic mixtures of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref25)  [stearic acid-n-butyramide/n-octanamide as phase change materials for low](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref25) [temperature solar heat storage. Appl Therm Eng 2017;111:1052](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref25)–9.
- [26] [Voelker C, Kornadt O, Ostry M. Temperature reduction due to the application of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref26)  [phase change materials. Energy Build 2008;40:937](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref26)–44.
- [27] [Guldentops G, Ardito G, Tao M, Granados-Focil S, Van Dessel S. A numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref27)  [study of adaptive building enclosure systems using solid](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref27)–solid phase change [materials with variable transparency. Energy Build 2018;167:240](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref27)–52.
- [28] [Cheng W, Xie B, Zhang R, Xu Z, Xia Y. Effect of thermal conductivities of shape](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref28)  [stabilized PCM on under-floor heating system. Appl Energy 2015;144:10](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref28)–8.
- [29] [Fazilati MA, Alemrajabi AA. Phase change material for enhancing solar water](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref29)  [heater, an experimental approach. Energy Convers Manag 2013;71:138](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref29)–45.
- [30] [Koca A, Oztop HF, Koyun T, Varol Y. Energy and exergy analysis of a latent heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref30)  [storage system with phase change material for a solar collector. Renew Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref30) [2008;33:567](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref30)–74.
- [31] [Coccia G, Di Nicola G, Tomassetti S, Pierantozzi M, Chieruzzi M, Torre L.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref31) [Experimental validation of a high-temperature solar box cooker with a solar-salt](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref31)[based thermal storage unit. Sol Energy 2018;170:1016](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref31)–25.
- [32] [Zhao L, Luo J, Wang H, Song G, Tang G. Self-assembly fabrication of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref32) [microencapsulated n-octadecane with natural silk fibroin shell for thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref32)[regulating textiles. Appl Therm Eng 2016;99:495](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref32)–501.
- [33] [Shaid A, Wang L, Padhye R. The thermal protection and comfort properties of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref33)  [aerogel and PCM-coated fabric for firefighter garment. J Ind Text 2016;45:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref33) [611](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref33)–25.
- [34] [Merlin K, Soto J, Delaunay D, Traonvouez L. Industrial waste heat recovery using](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref34)  [an enhanced conductivity latent heat thermal energy storage. Appl Energy 2016;](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref34)  [183:491](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref34)–503.

- <span id="page-25-0"></span>[35] [Nomura T, Okinaka N, Akiyama T. Waste heat transportation system, using phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref35)  [change material \(PCM\) from steelworks to chemical plant. Resour Conserv Recycl](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref35)  [2010;54:1000](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref35)–6.
- [36] [Emam M, Ookawara S, Ahmed M. Thermal management of electronic devices and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref36)  [concentrator photovoltaic systems using phase change material heat sinks:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref36)  [experimental investigations. Renew Energy 2019;141:322](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref36)–39.
- [37] [Fok S, Shen W, Tan F. Cooling of portable hand-held electronic devices using](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref37) [phase change materials in finned heat sinks. Int J Therm Sci 2010;49:109](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref37)–17.
- [38] [Kürklü A. Energy storage applications in greenhouses by means of phase change](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref38)  [materials \(PCMs\): a review. Renew Energy 1998;13:89](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref38)–103.
- [39] Hoang H-M, Leducq D, P´[erez-Masia R, Lagaron J, Gogou E, Taoukis P, et al. Heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref39)  [transfer study of submicro-encapsulated PCM plate for food packaging](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref39) [application. Int J Refrig 2015;52:151](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref39)–60.
- [40] [Leducq D, Ndoye F, Alvarez G. Phase change material for the thermal protection](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref40)  [of ice cream during storage and transportation. Int J Refrig 2015;52:133](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref40)–9.
- [41] [Swanson TD, Birur GC. NASA thermal control technologies for robotic spacecraft.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref41)  [Appl Therm Eng 2003;23:1055](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref41)–65.
- [42] [Gschwander S, Schossig P, Henning H-M. Micro-encapsulated paraffin in phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref42)[change slurries. Sol Energy Mater Sol Cells 2005;89:307](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref42)–15.
- [43] [Lin Y, Jia Y, Alva G, Fang G. Review on thermal conductivity enhancement,](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref43)  [thermal properties and applications of phase change materials in thermal energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref43)  [storage. Renew Sustain Energy Rev 2018;82:2730](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref43)–42.
- [44] [Junghanss T, Um Boock A, Vogel M, Schuette D, Weinlaeder H, Pluschke G. Phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref44)  [change material for thermotherapy of Buruli ulcer: a prospective observational](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref44) [single centre proof-of-principle trial. PLoS Neglected Trop Dis 2009;3:e380.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref44)
- [45] [Shao J, Darkwa J, Kokogiannakis G. Review of phase change emulsions \(PCMEs\)](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref45)  [and their applications in HVAC systems. Energy Build 2015;94:200](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref45)–17.
- [46] [Krishna J, Kishore P, Solomon AB. Heat pipe with nano enhanced-PCM for](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref46)  [electronic cooling application. Exp Therm Fluid Sci 2017;81:84](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref46)–92.
- [47] [Al-Rashed AA, Alnaqi AA, Alsarraf J. Energy-saving of building envelope using](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref47) [passive PCM technique: a case study of Kuwait City climate conditions. Sustain](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref47) [Energy Technol Assessments 2021;46:101254.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref47)
- [48] [Mahdaoui M, Hamdaoui S, Msaad AA, Kousksou T, El Rhafiki T, Jamil A, et al.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref48) [Building bricks with phase change material \(PCM\): thermal performances.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref48)  [Construct Build Mater 2021;269:121315](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref48).
- [49] [Li J, Zhang W, Xie L, Li Z, Wu X, Zhao O, et al. A hybrid photovoltaic and water/](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref49)  [air based thermal \(PVT\) solar energy collector with integrated PCM for building](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref49)  [application. Renew Energy 2022;199:662](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref49)–71.
- [50] [Elarem R, Alqahtani T, Mellouli S, Aich W, Khedher NB, Kolsi L, et al. Numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref50)  [study of an Evacuated Tube Solar Collector incorporating a Nano-PCM as a latent](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref50)  [heat storage system. Case Stud Therm Eng 2021;24:100859](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref50).
- [51] [Hu C, Wang Z, Bo R, Li C, Meng X. Effect of the cooling clothing integrating with](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref51)  [phase change material on the thermal comfort of healthcare workers with](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref51)  [personal protective equipment during the COVID-19. Case Stud Therm Eng 2023;](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref51)  [42:102725.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref51)
- [52] [Zhao Y, Zhang X, Xu X, Zhang S. Development of composite phase change cold](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref52)  [storage material and its application in vaccine cold storage equipment. J Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref52)  [Storage 2020;30:101455](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref52).
- [53] [Kurhade A, Talele V, Rao TV, Chandak A, Mathew V. Computational study of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref53)  [PCM cooling for electronic circuit of smart-phone. Mater Today Proc 2021;47:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref53)  [3171](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref53)–6.
- [54] [Li D, Wang J, Ding Y, Yao H, Huang Y. Dynamic thermal management for](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref54) [industrial waste heat recovery based on phase change material thermal storage.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref54) [Appl Energy 2019;236:1168](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref54)–82.
- [55] [Badji A, Benseddik A, Bensaha H, Boukhelifa A, Bouhoun S, Nettari C, et al.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref55)  [Experimental assessment of a greenhouse with and without PCM thermal storage](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref55)  [energy and prediction their thermal behavior using machine learning algorithms.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref55)  [J Energy Storage 2023;71:108133](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref55).
- [56] [Lamberg P, Lehtiniemi R, Henell A-M. Numerical and experimental investigation](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref56)  [of melting and freezing processes in phase change material storage. Int J Therm](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref56)  [Sci 2004;43:277](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref56)–87.
- [57] [Crank J, Crank J. Free and moving boundary problems. USA: Oxford University](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref57)  [Press; 1984.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref57)
- [58] [Hale Jr N, Viskanta R. Solid-liquid phase-change heat transfer and interface](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref58)  [motion in materials cooled or heated from above or below. Int J Heat Mass Tran](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref58)  [1980;23:283](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref58)–92.
- [59] Mnozisik. ¨ [Heat conduction. New York: John Wiley and sons; 1980.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref59)
- [60] [Zhang Y, Hu H, Kong X. Phase change energy storage-theory and application.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref60)  [Hefei: Press of University of Science and Technology of China; 1996. p. 8](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref60)–33.
- [61] [Goodman TR. The heat-balance integral and its application to problems involving](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref61)  [a change of phase. Trans Am Soc Mech Eng 1958;80:335](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref61)–42.
- [62] [Sadoun N, Si-Ahmed E-K, Colinet P. On the refined integral method for the one](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref62)[phase Stefan problem with time-dependent boundary conditions. Appl Math](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref62) [Model 2006;30:531](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref62)–44.
- [63] [Fabre A, Hristov J. On the integral-balance approach to the transient heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref63)  [conduction with linearly temperature-dependent thermal diffusivity. Heat Mass](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref63) [Tran 2017;53:177](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref63)–204.
- [64] [Ren H-S. Application of the heat-balance integral to an inverse Stefan problem.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref64)  [Int J Therm Sci 2007;46:118](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref64)–27.
- [65] [Riley D, Duck P. Application of the heat-balance integral method to the freezing](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref65)  [of a cuboid. Int J Heat Mass Tran 1977;20:294](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref65)–6.
- [66] [Bell G. A refinement of the heat balance integral method applied to a melting](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref66)  [problem. Int J Heat Mass Tran 1978;21:1357](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref66)–62.
- [67] Ahmad M, Bontemps A, Sall´[ee H, Quenard D. Experimental investigation and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref67) [computer simulation of thermal behaviour of wallboards containing a phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref67)  [change material. Energy Build 2006;38:357](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref67)–66.

- [68] [Goodman TR, Shea JJ. The melting of finite slabs. J Appl Mech 1960;27:16](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref68)–24.
- [69] [Caldwell J, Kwan Y. On the perturbation method for the Stefan problem with](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref69)  [time-dependent boundary conditions. Int J Heat Mass Tran 2003;46:1497](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref69)–501.
- [70] [Jamal-Abad MT, Saedodin S, Aminy M. Heat transfer in concentrated solar air](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref70)[heaters filled with a porous medium with radiation effects: a perturbation](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref70)  [solution. Renew Energy 2016;91:147](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref70)–54.
- [71] [Zeshao C. A simple method to solve the heat conduction problem of solidification](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref71)  [phase change - the thermal resistance method. J Univ Sci Technol China 1991;21:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref71)  69–[76.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref71)
- [72] [Voller V, Cross M. Accurate solutions of moving boundary problems using the](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref72)  [enthalpy method. Int J Heat Mass Tran 1981;24:545](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref72)–56.
- [73] [Hogge M, Gerrekens P. One-dimensional finite element analysis of thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref73)  [ablation with pyrolysis. Comput Methods Appl Mech Eng 1982;33:609](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref73)–34.
- [74] [Lewis R, Ravindran K. Finite element simulation of metal casting. Int J Numer](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref74) [Methods Eng 2000;47:29](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref74)–59.
- [75] [Lazaridis A. A numerical solution of the multidimensional solidification \(or](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref75) [melting\) problem. Int J Heat Mass Tran 1970;13:1459](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref75)–77.
- [76] [Crank J. Two methods for the numerical solution of moving-boundary problems](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref76)  [in diffusion and heat flow. Q J Mech Appl Math 1957;10:220](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref76)–31.
- [77] [Mitchell SL, Myers TG. Approximate solution methods for one-dimensional](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref77)
- [solidification from an incoming fluid. Appl Math Comput 2008;202:311](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref77)–26.
- [78] [Landau HG. Heat conduction in a melting solid. Q Appl Math 1950;8:81](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref78)–94.
- [79] [Voller VR, Swaminathan C, Thomas BG. Fixed grid techniques for phase change](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref79) [problems: a review. Int J Numer Methods Eng 1990;30:875](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref79)–98.
- [80] [Voller VR, Prakash C. A fixed grid numerical modelling methodology for](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref80)  [convection-diffusion mushy region phase-change problems. Int J Heat Mass Tran](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref80)  [1987;30:1709](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref80)–19.
- [81] [Rakotondrandisa A, Sadaka G, Danaila I. A finite-element toolbox for the](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref81)  simulation of solid–[liquid phase-change systems with natural convection. Comput](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref81)  [Phys Commun 2020;253:107188](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref81).
- [82] [Xiao W. Preparation and performance of cold storage phase change material for](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref82)  [high temperature cooling application. J Shanghai Jiao Tong Univ \(Sci\) 2013;47:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref82)  [1275](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref82).
- [83] [Zhang Y, Sun X, Medina MA. Calculation of transient phase change heat transfer](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref83)  [through building envelopes: an improved enthalpy model and error analysis.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref83) [Energy Build 2020;209:109673](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref83).
- [84] [Biswas K, Lu J, Soroushian P, Shrestha S. Combined experimental and numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref84)  [evaluation of a prototype nano-PCM enhanced wallboard. Appl Energy 2014;131:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref84)  [517](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref84)–29.
- [85] Kuboth S, Konig-Haagen ¨ [A, Brüggemann D. Numerical analysis of shell-and-tube](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref85)  [type latent thermal energy storage performance with different arrangements of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref85)  [circular fins. Energies 2017;10:274.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref85)
- [86] [Bas¸al B, Ünal A. Numerical evaluation of a triple concentric-tube latent heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref86) [thermal energy storage. Sol Energy 2013;92:196](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref86)–205.
- [87] [dos Santos FS, Ismail KA, Lino FA, Arabkoohsar A, Lago TG. Parametric](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref87) [investigation of the enhancing effects of finned tubes on the solidification of PCM.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref87)  [Int J Heat Mass Tran 2020;152:119485](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref87).
- [88] [Gorzin M, Hosseini MJ, Ranjbar AA, Bahrampoury R. Investigation of PCM](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref88) [charging for the energy saving of domestic hot water system. Appl Therm Eng](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref88)  [2018;137:659](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref88)–68.
- [89] [Ding Z, Jiang Z, Liu W, Wang J, Zhang Y. The influence of channels per square](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref89)  [inch on the freezing progress of the square copper column array water composite](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref89)  [PCM. J Energy Storage 2019;26:100848](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref89).
- [90] [Loem S, Deethayat T, Asanakham A, Kiatsiriroat T. Study on phase change](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref90) [material thermal characteristics during air charging/discharging for energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref90)  [saving of air-conditioner. Heat Mass Tran 2020;56:2121](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref90)–33.
- [91] [El Mankibi M, Zhai ZJ, Al-Saadi SN, Zoubir A. Numerical modeling of thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref91) [behaviors of active multi-layer living wall. Energy Build 2015;106:96](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref91)–110.
- [92] [Merlin K, Delaunay D, Soto J, Traonvouez L. Heat transfer enhancement in latent](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref92)  [heat thermal storage systems: comparative study of different solutions and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref92) [thermal contact investigation between the exchanger and the PCM. Appl Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref92)  [2016;166:107](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref92)–16.
- [93] [Jin X, Hu H, Shi X, Zhou X, Zhang X. Comparison of two numerical heat transfer](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref93)  [models for phase change material board. Appl Therm Eng 2018;128:1331](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref93)–9.
- [94] [Alawadhi EM. A solidification process with free convection of water in an](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref94) [elliptical enclosure. Energy Convers Manag 2009;50:360](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref94)–4.
- [95] [Regin AF, Solanki S, Saini J. An analysis of a packed bed latent heat thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref95) [energy storage system using PCM capsules: numerical investigation. Renew](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref95)  [Energy 2009;34:1765](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref95)–73.
- [96] [Alawadhi EM. Phase change process with free convection in a circular enclosure:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref96)  [numerical simulations. Comput Fluids 2004;33:1335](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref96)–48.
- [97] [Han P, Zheng X-H, Hou W-S, Qiu L, Tang D-W. Study on heat-storage and release](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref97)  [characteristics of multi-cavity-structured phase-change microcapsules. Phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref97)  [Transitions 2015;88:704](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref97)–15.
- [98] [Borderon J, Virgone J, Cantin R. Modeling and simulation of a phase change](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref98)  [material system for improving summer comfort in domestic residence. Appl](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref98) [Energy 2015;140:288](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref98)–96.
- [99] [Artinov A, Bachmann M, Rethmeier M. Equivalent heat source approach in a 3D](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref99)  [transient heat transfer simulation of full-penetration high power laser beam](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref99) [welding of thick metal plates. Int J Heat Mass Tran 2018;122:1003](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref99)–13.
- [100] [Khattari Y, El Rhafiki T, Choab N, Kousksou T, Alaphilippe M, Zeraouli Y.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref100)  [Apparent heat capacity method to investigate heat transfer in a composite phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref100)  [change material. J Energy Storage 2020;28:101239](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref100).
- [101] [Bouhal T, El Rhafiki T, Kousksou T, Jamil A, Zeraouli Y. PCM addition inside solar](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref101)  [water heaters: numerical comparative approach. J Energy Storage 2018;19:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref101) [232](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref101)–46.

- <span id="page-26-0"></span>[102] [Rabin Y, Korin E. An efficient numerical solution for the multidimensional](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref102)  [solidification \(or melting\) problem using a microcomputer. Int J Heat Mass Tran](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref102)  [1993;36:673](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref102)–83.
- [103] [Copertaro B, Principi P, Fioretti R. Thermal performance analysis of PCM in](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref103) [refrigerated container envelopes in the Italian context](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref103)–Numerical modeling and [validation. Appl Therm Eng 2016;102:873](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref103)–81.
- [104] [Jin X, Zhang X. Thermal analysis of a double layer phase change material floor.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref104) [Appl Therm Eng 2011;31:1576](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref104)–81.
- [105] [Zhang Y. Modified computational methods using effective heat capacity model for](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref105)  [the thermal evaluation of PCM outfitted walls. Int Commun Heat Mass Tran 2019;](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref105)  [108:104278.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref105)
- [106] [Bottarelli M, Bortoloni M, Su Y, Yousif C, Aydın AA, Georgiev A. Numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref106)  [analysis of a novel ground heat exchanger coupled with phase change materials.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref106)  [Appl Therm Eng 2015;88:369](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref106)–75.
- [107] [Li E, Liu G, Tan V, He Z. An efficient algorithm for phase change problem in tumor](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref107)  treatment using α[FEM. Int J Therm Sci 2010;49:1954](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref107)–67.
- [108] [Purlis E, Salvadori VO. Bread baking as a moving boundary problem. Part 1:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref108)  [mathematical modelling. J Food Eng 2009;91:428](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref108)–33.
- [109] [Jeong W, Seong J. Comparison of effects on technical variances of computational](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref109)  [fluid dynamics \(CFD\) software based on finite element and finite volume](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref109) [methods. Int J Mech Sci 2014;78:19](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref109)–26.
- [110] De Gracia A, Oro ´ [E, Farid M, Cabeza L. Thermal analysis of including phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref110) [change material in a domestic hot water cylinder. Appl Therm Eng 2011;31:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref110) [3938](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref110)–45.
- [111] [Comini dG, Del Guidice S, Lewis R, Zienkiewicz O. Finite element solution of non](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref111)[linear heat conduction problems with special reference to phase change. Int J](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref111)  [Numer Methods Eng 1974;8:613](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref111)–24.
- [112] [Sarkar A, Sastri V. Heat transfer during melting in rectangular enclosures](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref112)—a [finite element analysis. Int J Numer Methods Fluid 1992;14:83](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref112)–93.
- [113] [Liu C, Zhou Y, Li D, Meng F, Zheng Y, Liu X. Numerical analysis on thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref113)  [performance of a PCM-filled double glazing roof. Energy Build 2016;125:267](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref113)–75.
- [114] [Civan F. Practical implementation of the finite-analytic method. Appl Math Model](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref114)  [1995;19:298](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref114)–306.
- [115] [Raabe D. Overview of the lattice Boltzmann method for nano-and microscale fluid](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref115)  [dynamics in materials science and engineering. Model Simulat Mater Sci Eng](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref115)  [2004;12:13](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref115)–46.
- [116] Qian YH, d'Humi`[eres D, Lallemand P. Lattice BGK models for Navier-Stokes](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref116) [equation. Europhys Lett 1992;17:479](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref116)–84.
- [117] [Tao Y, You Y, He Y. Lattice Boltzmann simulation on phase change heat transfer](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref117)  [in metal foams/paraffin composite phase change material. Appl Therm Eng 2016;](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref117)  [93:476](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref117)–85.
- [118] [Huo Y, Rao Z. Investigation of solid-liquid phase change in the spherical capsule](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref118)  [using axisymmetric lattice Boltzmann model. Int J Heat Mass Tran 2018;119:1](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref118)–9.
- [119] [Monaghan JJ. An introduction to SPH. Comput Phys Commun 1988;48:89](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref119)–96.
- [120] [Koshizuka S, Oka Y. Moving-particle semi-implicit method for fragmentation of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref120)  [incompressible fluid. Nucl Sci Eng 1996;123:421](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref120)–34.
- [121] Onate ˜ [E, Idelsohn S, Zienkiewicz O, Taylor R. A finite point method in](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref121)  [computational mechanics. Applications to convective transport and fluid flow. Int](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref121)  [J Numer Methods Eng 1996;39:3839](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref121)–66.
- [122] [Allouche Y, Varga S, Bouden C, Oliveira AC. Validation of a CFD model for the](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref122) [simulation of heat transfer in a tubes-in-tank PCM storage unit. Renew Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref122)  [2016;89:371](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref122)–9.
- [123] [Ferfera RS, Madani B. Thermal characterization of a heat exchanger equipped](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref123) [with a combined material of phase change material and metallic foams. Int J Heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref123)  [Mass Tran 2020;148:119162](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref123).
- [124] [Aziz S, Amin N, Majid MA, Belusko M, Bruno F. CFD simulation of a TES tank](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref124)  [comprising a PCM encapsulated in sphere with heat transfer enhancement. Appl](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref124)  [Therm Eng 2018;143:1085](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref124)–92.
- [125] Kasibhatla RR, Konig-Haagen ¨ [A, Brüggemann D. Numerical modelling of wetting](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref125)  [phenomena during melting of PCM. Procedia Eng 2016;157:139](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref125)–47.
- [126] [Al-Abidi AA, Mat SB, Sopian K, Sulaiman M, Mohammed AT. CFD applications for](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref126)  [latent heat thermal energy storage: a review. Renew Sustain Energy Rev 2013;20:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref126)  [353](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref126)–63.
- [127] [Wang H, Wang H, Gao F, Zhou P, Zhai ZJ. Literature review on pressure](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref127)–velocity [decoupling algorithms applied to built-environment CFD simulation. Build](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref127) [Environ 2018;143:671](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref127)–8.
- [128] [Leonard BP. A stable and accurate convective modelling procedure based on](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref128) [quadratic upstream interpolation. Comput Methods Appl Mech Eng 1979;19:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref128)  [59](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref128)–98.
- [129] [Yang M, Tao WQ, Ozoe H. Computation and comparison for heat and fluid flow](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref129)  [using a QUICK and other difference schemes. Kyushu: The reports of Institute of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref129)  [Advanced Material Study Kyushu University; 1998. p. 1](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref129)–6.
- [130] [Ehms JN, Oliveski RDC, Rocha LO, Biserni C. Theoretical and numerical analysis](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref130)  [on phase change materials \(PCM\): a case study of the solidification process of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref130) [erythritol in spheres. Int J Heat Mass Tran 2018;119:523](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref130)–32.
- [131] [Valdes-Parada FJ, Ochoa-Tapia JA, Alvarez-Ramirez J. Validity of the](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref131)  permeability Carman–[Kozeny equation: a volume averaging approach. Physica A](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref131)  [2009;388:789](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref131)–98.
- [132] [Hu Z, Li A, Gao R, Yin H. Enhanced heat transfer for PCM melting in the frustum](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref132)[shaped unit with multiple PCMs. J Therm Anal Calorim 2015;120:1407](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref132)–16.
- [133] [Yang B, Raza A, Bai F, Zhang T, Wang Z. Microstructural evolution within mushy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref133)  zone during paraffin'[s melting and solidification. Int J Heat Mass Tran 2019;141:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref133)  [769](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref133)–78.
- [134] [Soliman AS, Sultan AA, Sultan MA. Effect of mushy zone parameter on phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref134)  [change behavior of different configurations storage unit: numerical simulation](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref134) [and experimental validation. Sustainability 2022;14:14540.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref134)

- [135] [Archibold AR, Rahman MM, Goswami DY, Stefanakos EK. Analysis of heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref135)  [transfer and fluid flow during melting inside a spherical container for thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref135) [energy storage. Appl Therm Eng 2014;64:396](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref135)–407.
- [136] [Parry AJ, Eames PC, Agyenim FB. Modeling of thermal energy storage shell-and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref136)[tube heat exchanger. Heat Tran Eng 2014;35:1](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref136)–14.
- [137] [Joybari MM, Haghighat F, Seddegh S. Numerical investigation of a triplex tube](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref137) [heat exchanger with phase change material: simultaneous charging and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref137) [discharging. Energy Build 2017;139:426](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref137)–38.
- [138] [Vogel J, Felbinger J, Johnson M. Natural convection in high temperature flat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref138) [plate latent heat thermal energy storage systems. Appl Energy 2016;184:184](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref138)–96.
- [139] [Jung U-H, Kim J-H, Kim J-H, Peck J-H, Kang C-D, Choi Y-S. Numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref139) [investigation on the melting of circular finned PCM system using CFD](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref139) & full [factorial design. J Mech Sci Technol 2016;30:2813](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref139)–26.
- [140] [Pahamli Y, Hosseini MJ, Ranjbar AA, Bahrampoury R. Analysis of the effect of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref140) [eccentricity and operational parameters in PCM-filled single-pass shell and tube](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref140)  [heat exchangers. Renew Energy 2016;97:344](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref140)–57.
- [141] [Sebti SS, Mastiani M, Mirzaei H, Dadvand A, Kashani S, Hosseini SA. Numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref141) [study of the melting of nano-enhanced phase change material in a square cavity.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref141)  [J Zhejiang Univ - Sci 2013;14:307](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref141)–16.
- [142] [Solomon L, Elmozughi AF, Oztekin A, Neti S. Effect of internal void placement on](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref142)  the heat transfer performance–[Encapsulated phase change material for energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref142) [storage. Renew Energy 2015;78:438](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref142)–47.
- [143] [Hosseini M, Rahimi M, Bahrampoury R. Experimental and computational](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref143)  [evolution of a shell and tube heat exchanger as a PCM thermal storage system. Int](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref143)  [Commun Heat Mass Tran 2014;50:128](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref143)–36.
- [144] [Abdulrahman RS, Ibrahim FA, Dakhil SF. Development of paraffin wax as phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref144)  [change material based latent heat storage in heat exchanger. Appl Therm Eng](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref144) [2019;150:193](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref144)–9.
- [145] [Yadav A, Samir S. Experimental and numerical investigation of spatiotemporal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref145)  [characteristics of thermal energy storage system in a rectangular enclosure.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref145) [J Energy Storage 2019;21:405](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref145)–17.
- [146] [Li X-Y, Qu D-Q, Yang L, Li K-D. Experimental and numerical investigation of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref146) [discharging process of direct contact thermal energy storage for use in](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref146) [conventional air-conditioning systems. Appl Energy 2017;189:211](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref146)–20.
- [147] [Li W, Li S-G, Guan S, Wang Y, Zhang X, Liu X. Numerical study on melt fraction](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref147)  [during melting of phase change material inside a sphere. Int J Hydrogen Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref147)  [2017;42:18232](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref147)–9.
- [148] [Zheng H, Wang C, Liu Q, Tian Z, Fan X. Thermal performance of copper foam/](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref148) [paraffin composite phase change material. Energy Convers Manag 2018;157:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref148) [372](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref148)–81.
- [149] [Al-Abidi AA, Mat S, Sopian K, Sulaiman M, Mohammad AT. Internal and external](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref149)  [fin heat transfer enhancement technique for latent heat thermal energy storage in](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref149)  [triplex tube heat exchangers. Appl Therm Eng 2013;53:147](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref149)–56.
- [150] [Al-Abidi AA, Mat S, Sopian K, Sulaiman M, Mohammad AT. Numerical study of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref150)  [PCM solidification in a triplex tube heat exchanger with internal and external fins.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref150)  [Int J Heat Mass Tran 2013;61:684](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref150)–95.
- [151] [Yang X, Lu Z, Bai Q, Zhang Q, Jin L, Yan J. Thermal performance of a shell-and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref151)[tube latent heat thermal energy storage unit: role of annular fins. Appl Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref151)  [2017;202:558](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref151)–70.
- [152] [Zhang C, Li J, Chen Y. Improving the energy discharging performance of a latent](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref152)  [heat storage \(LHS\) unit using fractal-tree-shaped fins. Appl Energy 2020;259:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref152)  [114102](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref152).
- [153] [Kheradmand M, Azenha M, de Aguiar JL, Castro-Gomes J. Experimental and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref153) [numerical studies of hybrid PCM embedded in plastering mortar for enhanced](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref153) [thermal behaviour of buildings. Energy 2016;94:250](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref153)–61.
- [154] [Zhong K, Li S, Sun G, Li S, Zhang X. Simulation study on dynamic heat transfer](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref154) [performance of PCM-filled glass window with different thermophysical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref154) [parameters of phase change material. Energy Build 2015;106:87](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref154)–95.
- [155] [Gowreesunker B, Stankovic S, Tassou S, Kyriacou P. Experimental and numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref155)  [investigations of the optical and thermal aspects of a PCM-glazed unit. Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref155)  [Build 2013;61:239](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref155)–49.
- [156] [Li S, Zou K, Sun G, Zhang X. Simulation research on the dynamic thermal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref156) [performance of a novel triple-glazed window filled with PCM. Sustain Cities Soc](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref156)  [2018;40:266](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref156)–73.
- [157] [Liu F-h, Xu J-x, Wang H-t, Wang H. Numerical method and model for calculating](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref157)  [thermal storage time for an annular tube with phase change material. J Cent](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref157)  [South Univ 2017;24:217](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref157)–26.
- [158] [Caliano M, Bianco N, Graditi G, Mongibello L. Analysis of a phase change](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref158)  [material-based unit and of an aluminum foam/phase change material composite](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref158)[based unit for cold thermal energy storage by numerical simulation. Appl Energy](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref158)  [2019;256:113921](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref158).
- [159] [Seddegh S, Wang X, Henderson AD. Numerical investigation of heat transfer](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref159)  [mechanism in a vertical shell and tube latent heat energy storage system. Appl](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref159) [Therm Eng 2015;87:698](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref159)–706.
- [160] [Fornarelli F, Camporeale SM, Fortunato B, Torresi M, Oresta P, Magliocchetti L,](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref160) [et al. CFD analysis of melting process in a shell-and-tube latent heat storage for](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref160) [concentrated solar power plants. Appl Energy 2016;164:711](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref160)–22.
- [161] [Hosseini M, Ranjbar A, Sedighi K, Rahimi M. A combined experimental and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref161) [computational study on the melting behavior of a medium temperature phase](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref161) [change storage material inside shell and tube heat exchanger. Int Commun Heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref161)  [Mass Tran 2012;39:1416](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref161)–24.
- [162] [Yang X, Bai Q, Guo Z, Niu Z, Yang C, Jin L, et al. Comparison of direct numerical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref162)  [simulation with volume-averaged method on composite phase change materials](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref162) [for thermal energy storage. Appl Energy 2018;229:700](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref162)–14.
- [163] [Zhang C, Wu L, Chen Y. Study on solidification of phase change material in fractal](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref163)  [porous metal foam. Fractals 2015;23:1540003](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref163).

- <span id="page-27-0"></span>[164] [Sheikholeslami M, Lohrasbi S, Ganji DD. Numerical analysis of discharging](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref164)  [process acceleration in LHTESS by immersing innovative fin configuration using](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref164)  [finite element method. Appl Therm Eng 2016;107:154](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref164)–66.
- [165] [Sciacovelli A, Gagliardi F, Verda V. Maximization of performance of a PCM latent](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref165)  [heat storage system with innovative fins. Appl Energy 2015;137:707](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref165)–15.
- [166] [Eslamnezhad H, Rahimi AB. Enhance heat transfer for phase-change materials in](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref166)  [triplex tube heat exchanger with selected arrangements of fins. Appl Therm Eng](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref166)  [2017;113:813](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref166)–21.
- [167] [Darzi AR, Farhadi M, Sedighi K. Numerical study of melting inside concentric and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref167)  [eccentric horizontal annulus. Appl Math Model 2012;36:4080](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref167)–6.
- [168] [Jang SP, Choi SU. Role of Brownian motion in the enhanced thermal conductivity](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref168)  [of nanofluids. Appl Phys Lett 2004;84:4316](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref168)–8.
- [169] [Bose P, Amirtham VA. A review on thermal conductivity enhancement of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref169) [paraffinwax as latent heat energy storage material. Renew Sustain Energy Rev](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref169) [2016;65:81](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref169)–100.
- [170] [Khodadadi J, Hosseinizadeh S. Nanoparticle-enhanced phase change materials](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref170)  [\(NEPCM\) with great potential for improved thermal energy storage. Int Commun](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref170)  [Heat Mass Tran 2007;34:534](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref170)–43.
- [171] [Boujelbene M, Mohammed HI, Majdi HS, Babaei-Mahani R, Talebizadehsardari P,](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref171)  [Rahbari A. Melting performance of nano-enhanced phase change materials in a](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref171) [triple-tube heat exchanger with zigzag-shaped tubes. J Energy Storage 2023;67:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref171)  [107484](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref171).

- [172] [Eisapour M, Eisapour AH, Shafaghat A, Mohammed HI, Talebizadehsardari P,](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref172)  [Chen Z. Solidification of a nano-enhanced phase change material \(NePCM\) in a](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref172) [double elliptical latent heat storage unit with wavy inner tubes. Sol Energy 2022;](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref172)  [241:39](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref172)–53.
- [173] [Kashani S, Lakzian E, Lakzian K, Mastiani M. Numerical analysis of melting of](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref173) [nano-enhanced phase change material in latent heat thermal energy storage](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref173)  [system. Therm Sci 2014;18:335](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref173)–45.
- [174] [Hosseinizadeh S, Darzi AR, Tan F. Numerical investigations of unconstrained](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref174) [melting of nano-enhanced phase change material \(NEPCM\) inside a spherical](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref174) [container. Int J Therm Sci 2012;51:77](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref174)–83.
- [175] [Arıcı M, Tütüncü E, Kan M, Karabay H. Melting of nanoparticle-enhanced paraffin](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref175)  [wax in a rectangular enclosure with partially active walls. Int J Heat Mass Tran](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref175)  [2017;104:7](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref175)–17.
- [176] [Dhaidan NS, Khodadadi J, Al-Hattab TA, Al-Mashat SM. Experimental and](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref176) [numerical investigation of melting of phase change material/nanoparticle](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref176) [suspensions in a square container subjected to a constant heat flux. Int J Heat](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref176)  [Mass Tran 2013;66:672](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref176)–83.
- [177] [Kashani S, Ranjbar A, Abdollahzadeh M, Sebti S. Solidification of nano-enhanced](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref177)  [phase change material \(NEPCM\) in a wavy cavity. Heat Mass Tran 2012;48:](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref177) [1155](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref177)–66.
- [178] [Valan AA, Sasmito AP, Mujumdar AS. Numerical performance study of paraffin](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref178) [wax dispersed with alumina in a concentric pipe latent heat storage system.](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref178)  [Therm Sci 2013;17:419](http://refhub.elsevier.com/S1364-0321(23)00581-6/sref178)–30.