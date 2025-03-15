Las funciones del archivo 'funciones.py' presentan una descripción sobre el output y 
sobre cada uno de sus argumentos.  


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#                           INDICE - HAY 12 FUNCIONES
#
#                 Las funciones construidas aquí tienen por objeto
#             completar un análisis de rentabilidad total (renta fija)
#                       quien se sintetiza en la función 12. 
#
#
# FUNCION 1: Línea 103. 
#            Nombre: tasabadlar
#            Descripción: Construye serie de tasa badlar esperada por REM del BCRA.
#
# FUNCION 2: Línea 167. 
#            Nombre: ffbonocap
#            Descripción: Construye el flujo de fondos de un activo de renta fija,
#                         hasta la fecha horizonte. Este activo debe ser o cupon 
#                         cero, bullet, o uno que paga capital y renta al vencimiento. 
#
# FUNCION 3: Línea 365. 
#            Nombre: ffbonodesc
#            Descripción: Construye el flujo de fondos de un activo de renta fija,
#                         luego de la fecha horizonte. Este activo debe ser o 
#                         cupon cero, bullet, o uno que paga capital y renta al 
#                         vencimiento. 
#
# FUNCION 4: Línea 564. 
#            Nombre: capflujos
#            Descripción: Capitaliza los flujos cobrados del bono hasta la fecha 
#                         de horizonte de inversión.
#
# FUNCION 5: Línea 700. 
#            Nombre: grafica_bonos
#            Descripción: Realiza la gráfica de dispersión de renta fija soberana 
#                         en pesos, en pesos CER, en pesos dólar linked, y en USD.
#                         También grafica las líneas de regresión simple correspondeintes. 
#
# FUNCION 6: Línea 831. 
#            Nombre: tabla_infla
#            Descripción: Realiza un dataframe con la inflación mensual esperada.
#                         La serie se extiende por una cantidad de meses que se 
#                         debe indicar. Para realizar la estimación, se utiliza 
#                         el mercado de renta fija en pesos y en pesos CER.
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (CER de diciembre).  
#
# FUNCION 7: Línea 1030. 
#            Nombre: tabla_dev
#            Descripción: Crea un DataFrame con la tasa de devaluación/depreciación 
#                         mensual esperada y también la acumulada correspondiente.
#                         La tasa de dev/dep se obtiene de una de tres fuentes:
#                         1) bonos USD versus bonos CER, 2) bonos en DL vs bonos 
#                         en pesos, y 3) futuros.
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (tca3500 de diciembre). 
#
# FUNCION 8: Línea 1227. 
#            Nombre: tabla_infla_esc
#            Descripción: Crea un DataFrame que contiene la serie de inflación
#                         esperada "arbitraria", es decir, es un escenario imagi-
#                         nado en función de un nivel base de inflación mensual y 
#                         una tasa de variación de este nivel en puntos porcen-
#                         tuales. 
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (CER de diciembre). 
#
# FUNCION 9: Línea 1373. 
#            Nombre: tabla_dev_esc
#            Descripción: Crea un DataFrame que contiene la serie de dev/dep
#                         esperada "arbitraria", es decir, es un escenario imagi-
#                         nado en función de un nivel base de dev/dep mensual y 
#                         una tasa de variación de este nivel en puntos porcentuales. 
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (tca3500 de diciembre).  
#
# FUNCION 10: Línea 1561.  
#             Nombre: flujobono_act 
#             Descripción: Genera el flujo de fondos actualizado de renta fija 
#                          hasta la fecha horizonte. Utilizando el flujo de fondos
#                          base, se aplica el índice CER o la tasa de dev/dep 
#                          segun corresponda. 
#    
# FUNCION 11: Línea 1758. 
#             Nombre: p_reventa 
#             Descripción: Genera el precio de reventa esperado de un activo de
#                          renta fija. Este precio se obtiene para la fecha hori-
#                          zonte.
#    
# FUNCION 12: Línea 1971.
#             Nombre: analisis_rt 
#             Descripción: Genera una tabla con todos los ticket de los bonos 
#                          bullet y las letras en pesos, pesos CER, y pesos DL,
#                          y para cada una se muestra su rendimiento total anual
#                          esperado, y los motivos que lo generan: cobro de cupones,
#                          cobro de intereses por reinversión, y cobro por reventa
#                          o por cobro de capital.   
