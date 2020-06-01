
This README file is meant to provide an overview about how to use the script (xenon_limits.cpp) that Marc sent me.





###########################################################
##### Marc's Mail #########################################
###########################################################


Hi Daniel,

hier ist ein script, dass die Basisfunktionalität hat. Es läuft unter ROOT:

> .L xenon_limits.cpp
> diffrate_int(40.,1e-47,1,5,50)

dies plotted Dir das SI-Spektrum eines 50 GeV WIMPs mit sigma=1e-47 cm²
und gibt Dir (in der Konsole) die Rate (in evts/kg/d) im Bereich von
5-50 keVnr aus. Es gibt noch mehr Funktionen, die sind am Anfang des
Skripts kurz erklärt.

Ciao
Marc





###########################################################
##### How to Use it #######################################
###########################################################


- source 'root':
  $ rootybooty
  ('rootybooty' is an alias I defined in '.bash_aliases' that is used to source 'root'.
   Maybe check if the root version that is sourced is also installed.)

- start script:
  $ root .L xenon_limits.cpp
  (This just loads the script. You can execute certain commands afterwards.)

- execute the desired function within root:
  $ diffrate_int(40.,1e-47,1,5,50)
  (This will plot the differential rate; the data you can then access with a data grabber.)





###########################################################
##### How to Use the Modified File ########################
###########################################################


Instead of grabbing the data from the plot generated with 'xenon_limits.cpp' one can just use the modified file 'xenon_limits_mod.cpp' and automatically generate a .txt file containing the plotted data.






