import sys
import os
import yaml
import math
import numpy
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------------
# INIT
#--------------------------------------------------------------------------------------------------

params_filepath = os.path.join(os.path.dirname(__file__), 'params-ka.yaml')

try:
    with open(params_filepath, encoding='utf-8') as file:
        params = yaml.safe_load(file)
except:
    print('Erro: caminho "' + params_filepath + '" não encontrado.')
    sys.exit(-1)

rpm = params['rpm']
torque_rpm = params['torque_rpm']
power_rpm = params['power_rpm']
e = params['e']
f = params['f']
cx = params['cx']
a_frontal = params['a_frontal']
rho = params['rho']
m = params['m']
g = params['g']
n_transm = params['n_transm']
r_d = params['r_d']
i_1 = params['i_1']
i_2 = params['i_2']
i_3 = params['i_3']
i_4 = params['i_4']
i_5 = params['i_5']
i_d = params['i_d']

#--------------------------------------------------------------------------------------------------
# CALC
#--------------------------------------------------------------------------------------------------

# Transformação de rotação do motor para velocidade na marcha 1
vel_1 = [((math.pi / 30) * (1 - e) * r_d / (i_1 * i_d)) * x for x in rpm]
# Transformação de rotação do motor para velocidade na marcha 2
vel_2 = [((math.pi / 30) * (1 - e) * r_d / (i_2 * i_d)) * x for x in rpm]
# Transformação de rotação do motor para velocidade na marcha 3
vel_3 = [((math.pi / 30) * (1 - e) * r_d / (i_3 * i_d)) * x for x in rpm]
# Transformação de rotação do motor para velocidade na marcha 4
vel_4 = [((math.pi / 30) * (1 - e) * r_d / (i_4 * i_d)) * x for x in rpm]
# Transformação de rotação do motor para velocidade na marcha 5
vel_5 = [((math.pi / 30) * (1 - e) * r_d / (i_5 * i_d)) * x for x in rpm]

# Conversão de m/s para km/h
vel_kmh_1 = [3.6 * x for x in vel_1]
vel_kmh_2 = [3.6 * x for x in vel_2]
vel_kmh_3 = [3.6 * x for x in vel_3]
vel_kmh_4 = [3.6 * x for x in vel_4]
vel_kmh_5 = [3.6 * x for x in vel_5]

# Todas velocidades em um array
vel = sorted(list(set([*vel_1, *vel_2, *vel_3, *vel_4, *vel_5])))
vel_kmh = [3.6 * x for x in vel]

power_after_transm_rpm = [n_transm * x for x in power_rpm] # Potência no cubo

G = m * g # Peso do veículo

# Potência da resistência ao rolamento
Pr_vel = [(((f * G) / (1 - e)) * x) / 1000 for x in vel]
# Potência da resistência aerodinâmica
Pa_vel = [((cx * a_frontal * 0.5 * rho) / (1 - e) * (x*x*x)) / 1000 for x in vel]
# Soma das potências de resistência ao rolamento e aerodinâmica
Pr_Pa_vel = numpy.add(Pr_vel, Pa_vel)

#--------------------------------------------------------------------------------------------------
# PLOT
#--------------------------------------------------------------------------------------------------

plt.figure(1)
plt.title('Curvas de torque e potência')
plt.plot(rpm, torque_rpm, 'b', label='Torque [Nm]')
plt.plot(rpm, power_rpm, 'r', label='Potência [kW]')
plt.xlabel('RPM')
plt.legend()

plt.figure(2)
plt.title('Velocidade do veículo nas diferentes marchas')
plt.plot(rpm, vel_kmh_1, label='Velocidade na marcha 1 [km/h]')
plt.plot(rpm, vel_kmh_2, label='Velocidade na marcha 2 [km/h]')
plt.plot(rpm, vel_kmh_3, label='Velocidade na marcha 3 [km/h]')
plt.plot(rpm, vel_kmh_4, label='Velocidade na marcha 4 [km/h]')
plt.plot(rpm, vel_kmh_5, label='Velocidade na marcha 5 [km/h]')
plt.xlabel('RPM')
plt.legend()

plt.figure(3)
plt.title('Curvas de potência no cubo nas diferentes marchas')
plt.plot(vel_kmh_1, power_after_transm_rpm, label='Potência na marcha 1 [kW]')
plt.plot(vel_kmh_2, power_after_transm_rpm, label='Potência na marcha 2 [kW]')
plt.plot(vel_kmh_3, power_after_transm_rpm, label='Potência na marcha 3 [kW]')
plt.plot(vel_kmh_4, power_after_transm_rpm, label='Potência na marcha 4 [kW]')
plt.plot(vel_kmh_5, power_after_transm_rpm, label='Potência na marcha 5 [kW]')
plt.xlabel('Velocidade [km/h]')
plt.legend()

plt.figure(4)
plt.title('Potências de resistência ao rolamento e aerodinâmica')
plt.plot(vel_kmh, Pr_vel, label='Potência de resistência ao rolamento [kW]')
plt.plot(vel_kmh, Pa_vel, label='Potência de arrasto aerodinâmico [kW]')
plt.xlabel('Velocidade [km/h]')
plt.legend()

plt.figure(5)
plt.title('Potências no cubo e de resistências')
plt.plot(vel_kmh_1, power_after_transm_rpm, label='Potência na marcha 1 [kW]')
plt.plot(vel_kmh_2, power_after_transm_rpm, label='Potência na marcha 2 [kW]')
plt.plot(vel_kmh_3, power_after_transm_rpm, label='Potência na marcha 3 [kW]')
plt.plot(vel_kmh_4, power_after_transm_rpm, label='Potência na marcha 4 [kW]')
plt.plot(vel_kmh_5, power_after_transm_rpm, label='Potência na marcha 5 [kW]')
plt.plot(vel_kmh, Pr_Pa_vel, label='Pa + Pr [kW]')
plt.xlabel('Velocidade [km/h]')
plt.legend()

plt.figure(6)
plt.title('Potências no cubo e de resistências')
plt.plot(vel_kmh_1, power_after_transm_rpm, label='Potência na marcha 1 [kW]')
plt.plot(vel_kmh_2, power_after_transm_rpm, label='Potência na marcha 2 [kW]')
plt.plot(vel_kmh_3, power_after_transm_rpm, label='Potência na marcha 3 [kW]')
plt.plot(vel_kmh_4, power_after_transm_rpm, label='Potência na marcha 4 [kW]')
plt.plot(vel_kmh_5, power_after_transm_rpm, label='Potência na marcha 5 [kW]')
plt.plot(vel_kmh, Pr_Pa_vel, label='Pa + Pr [kW]')
plt.vlines(158.5, 0, 100, linestyles="dashed")
plt.text(163.5, 60,'Vmax = 158.5 km/h', rotation=90)
plt.xlabel('Velocidade [km/h]')
plt.legend()

plt.show()
