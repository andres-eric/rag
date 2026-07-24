|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||

|**Actualizó:**|**Revisó/Aprobó:**|
|---|---|
|José David Verbel: Profesional Soporte TI|Sergio Domínguez Líder TI|  
|**SGCA023_5_1**||
|---|---|
|**Plan de contingencia de TI**||
|**2024-09-03**||
|**TABLA DE CONTENIDO**||
|**1** **OBJETIVO**|**4**|
|**2** **ALCANCE**|**4**|
|**3** **POLÍTICAS GENERALES**|**4**|
|**4** **CONTROLES PARA MITIGAR LOS RIESGOS**|**5**|
|**4.1** **FALLAS EN EL FLUIDO ELÉCTRICO**|**5**|
|**4.2** **FALLAS EN LAS COMUNICACIONES**|**6**|
|**4.3** **FALLAS EN LOS SERVIDORES**|**7**|
|**4.4** **SABOTAJE CAUSADO A LOS SISTEMAS DETI YCIBERATAQUES**|**8**|
|**5** **DESCRIPCIÓN DEL SERVICIO PRESTADO POR MVTEL A **|**9**|
|**6** **DESCRIPCIÓN DEL PROCESO DE COPIAS DE SEGURIDAD (BACKUP)**|**11**|
|**6.1** **PROCEDIMIENTOS DERESPALDO**|**11**|
|6.1.1 COPIAS DE SERVIDORES|11|
|6.1.2 COPIAS ADICIONALES|12|
|6.1.3 BACKUPS DE LA INFORMACIÓN DE LANAS BELENUS.|12|
|6.1.4 COPIAS DE SEGURIDADADICIONALES DE SISTEMA|13|
|6.1.5 BACKUP DECOMPUTADORES|13|
|6.1.6 BACKUP BASES DE DATOS|13|
|**6.2** **ALMACENAMIENTO DE LOSRESPALDOS**|**14**|
|**7** **DESCRIPCIÓN DEL SERVICIO DE TELEFONÍA**|**15**|
|**8** **CANALES Y CONTACTOS**|**16**|
|**8.1** **CANALES DE ATENCIÓN FRENTE A LOS RIESGOS DETI**|**16**|
||Página: 2|  
|**SGCA023_5_1**|
|---|
|**Plan de contingencia de TI**|
|**2024-09-03**|
|8.1.1 FALLAS EN EL FLUIDO ELÉCTRICO 16|
|8.1.2 FALLAS EN LAS COMUNICACIONES 16|
|8.1.3 FALLAS EN LOS SERVIDORES 17|
|8.1.4 SABOTAJE YCIBERATAQUES 17|
|**8.2** **PRINCIPALES PROVEEDORES DE SUMINISTROS Y SERVICIOS** **18**|
|**_8.3_** **CANALES DE COMUNICACIÓNMV-TEL SOPORTETI YSERVICIO DE TELEFONÍA** **18**|
|**9** **ACTIVACIÓN DE PROTOCOLOS Y PLAN DE SIMULACROS** **20**|
|**9.1** **PLAN PARA LA CONTINUIDAD DETI** **20**|
|**9.2** **PLAN DE SIMULACROSTI** **22**|
|**10** **PROGRAMACIÓN DE BACKUPS DE BD INSTANCIA SARASVATI** **23**|  
Página: 3  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||

Describir las acciones implementadas por la organización para garantizar la continuidad de los servicios de TI ante las posibles fallas que los afecten.

Este procedimiento es para uso exclusivo del personal del área de soporte tecnológico y aplica para ser ejecutado en la oficina central de **** sede Guarne – Antioquia. En él se define la manera de actuar ante las siguientes fallas:  
- Fallas en el fluido eléctrico  
- Fallas en las comunicaciones  
- Fallas en los servidores  
- Sabotaje causado a los sistemas de TI y Ciberataques  
Adicionalmente este procedimiento explica la interacción del proveedor MV-Tel en el soporte de los servicios de TI.

Este procedimiento es responsabilidad de la gerencia de tecnología y debe ser revisado anualmente por el proceso de tecnología para garantizar que los servicios de TI ofrecidos a los clientes internos y externos estén disponibles en el menor tiempo posible si se llegara a presentar alguna de las fallas listadas en el numeral 2.  
Los canales de atención ante los riegos de TI se describen en el numeral 8.1, y los contactos de los principales proveedores externos, reposición de equipos, suministro de repuestos, mantenimiento correctivo, etc, se relacionan en el numeral 8.2.  
Página: 4  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||

A continuación, se describen las acciones implementadas para mitigar cada uno de los riesgos que pueden afectar la continuidad de los servicios de TI.  
#### **4.1** Fallas en el fluido eléctrico  
Se tiene un sistema combinado de planta eléctrica y UPS que evita que ante una falla del fluido eléctrico de EPM, los servidores y equipos de red se apaguen inesperadamente, evitando así perder información no guardada o daños en los sistemas operativos. Igualmente, dichos respaldos de energía están disponibles para proveer servicio a algunos usuarios y servicios críticos, por un tiempo limitado, ante la ausencia principal de fluido eléctrico.  
El esquema de protección ante una falla eléctrica es el siguiente:  
##### **_Ilustración 1: Esquema de protección_**  
Descripción del funcionamiento:  
- Ante una falla en el fluido eléctrico de EPM, la planta eléctrica entra en funcionamiento de manera automática, evitando de este modo que los equipos que se encuentren conectados en la red regulada de la UPS pierdan alimentación y se apaguen inesperadamente.  
- Durante el tiempo que transcurre entre el corte de fluido eléctrico de EPM y el momento en que entra en operación la planta eléctrica, la UPS mantiene el suministro de energía requerido a los equipos críticos y/o sensibles a cortes de energía.  
Página: 5  
##### **SGCA023_5_1 Plan de contingencia de TI 2024-09-03**  
- La planta eléctrica da soporte a los centros de cómputo y algunos procesos fabriles críticos. A través de un contrato anual, la empresa EQUITEL se encarga de mantener la planta eléctrica en óptimas condiciones de funcionamiento. Semanalmente se hace un arranque de la planta para garantizar su disponibilidad y confiabilidad ante una falla prolongada en el fluido eléctrico de EPM. Cuenta con un tanque de combustible de 500 galones, el cual proporciona una autonomía de generación de 4 días aprox.  
- Las UPS instaladas son tipo On Line y garantizan una autonomía a full carga de 10 minutos, tiempo suficiente para apagar controladamente todos los equipos requeridos para los servicios de TI en Celsa y/o para la entrada de la planta eléctrica, la cual garantiza el fluido eléctrico de manera ininterrumpida a la UPS cuando se presente una falla en la red de EPM. La empresa Tronex se encarga de hacer los mantenimientos preventivos y/o correctivos.  
#### 4.2 Fallas en las comunicaciones  
Como protección ante una falla en las comunicaciones, Celsa tiene implementados dos enlaces de Internet con dos operadores diferentes y por medios físicos diferentes, a saber:  
- Enlace Tigo: Internet banda ancha UK por fibra óptica  
- Enlace GTD Colombia: Internet dedicado, UK por radio enlace  
Estos dos enlaces se reciben en un equipo de seguridad perimetral que distribuye una parte del tráfico por el enlace de Tigo y otra parte por el enlace de GTD Colombia, ante una falla de uno de los dos canales el equipo redirecciona el tráfico al otro enlace y se restablece luego de que se normaliza la operación del canal.  
##### **_Ilustración 2: Esquema de comunicaciones_**  
Página: 6  
**SGCA023_5_1**  
##### **2024-09-03**  
##### **Plan de contingencia de TI**  
#### 4.3 Fallas en los servidores  
Como protección ante una falla de los servidores, Celsa tiene implementado un esquema de réplica, en el cual se tiene un servidor principal que atiende los requerimientos de los usuarios de Celsa y un servidor secundario, al que se pueden trasladar los procesos ante una falla del principal.  
Esta funcionalidad permite que la información del servidor principal se replique en el secundario para asegurar que ambos tienen la misma información y cualquiera de los dos pueda dar servicio a los usuarios de Celsa.  
<mark>Este proceso se realiza en los servidores TARANIS y ZEUS los cuales presentan las mismas características.</mark>  
- <mark>El servidor TARANIS actúa como servidor activo y dispone de seis máquinas virtuales encendidas y en producción.</mark>  
- <mark>El servidor ZEUS actúa como servidor pasivo, recibe la copia de las seis máquinas virtuales.</mark>  
- <mark>Las máquinas virtuales son HERMES, HEFESTO, PENELOPE, SARASVATI, VALI y THOR.</mark>  
- <mark>La réplica consiste en la copia del contenido original a otra ubicación.</mark>  
El siguiente esquema ilustra la configuración de los servidores principal y de réplica implementado en Celsa  
##### **_Ilustración 3: Servicio de réplica_**  
Página: 7  
##### **SGCA023_5_1 Plan de contingencia de TI 2024-09-03**  
#### 4.4 Sabotaje causado a los sistemas de TI y Ciberataques  
Como protección ante posibles intentos de sabotaje o ataques desde Internet, se cuenta con un equipo UTM (2 Fortinet en alta disponibilidad) en el cual se tienen configurados grupos de navegación y se tiene restringido el acceso a sitios de pornografía, redes sociales, música y videos.  
Solo un pequeño grupo de usuarios tiene acceso a redes sociales o sitios de videos por la naturaleza de su rol al interior de Celsa y están autorizados previamente por sus jefes directos.  
Otra herramienta usada para la protección ante ataques es el antivirus, que se tiene instalado en todos los computadores conectados al dominio y que se usa para proteger la información de los usuarios y servidores de ataques de virus informáticos.  
Otra medida usada como protección contra ataques informáticos consiste en que el acceso a los servidores se tiene restringido solo a los usuarios que están dentro de la red de (LAN/WiFi) o que están por fuera, pero conectados por VPN (en este caso se puede decir que también están conectados dentro de la red de ). Además, los servidores no se encuentran publicados en Internet.  
Cuando un usuario requiere acceso remoto, es necesaria la autorización de su jefe, así como del área de tecnología de Celsa. Para esto se usa autenticación de la VPN en el equipo UTM y autenticación del dominio para asegurar que el usuario tiene los permisos adecuados para ingresar al servidor.  
Los equipos de usuario y servidores se mantienen con el antivirus actualizado, esta es una de las medidas más importantes para proteger los equipos y la red ante ataques de malware o sabotajes. Se realiza revisión periódica de los equipos desde la consola de administración del antivirus, con el fin de garantizar que se encuentren siempre usando la última versión y los últimos módulos de detección.  
Se tienen copias de respaldo de archivos y de bases de dato para restaurar la información en caso de sabotajes o ciberataques,  
Página: 8  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||

El alcance del servicio contratado por Celsa con MV-Tel es el siguiente:  
- Soporte remoto de Servidores (Hardware, sistema operativo y servicios de red) y seguridad perimetral (UMTS).  
- Soporte remoto de computadores de usuario final (Hardware, sistema operativo y aplicaciones MS Office)  
- Soporte de la infraestructura de Networking.  
- Administración del servicio de Correo Electrónico  
- Soporte del servicio de conexión a Internet  
- Soporte del respaldo de la información de los servidores  
El servicio se presta en la mayoría de los casos en forma remota desde la sede de MVTEL, pues se cuenta con un enlace VPN que permite conectar en forma segura los servidores con la red de MVTEL.  
El esquema de la conexión entre MVTEL y Celsa es el siguiente:  
##### **_Ilustración 4: Esquema conexión MvTel - Celsa_**  
Página: 9  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||  
Tanto en el lado de Celsa como de MVTEL se cuenta con equipos UTM que se encargan de asegurar la comunicación entre las dos redes y solo permiten la comunicación desde unos equipos específicos de la red de MV-Tel a los servidores de Celsa.  
Cuando se requiere soporte presencial en la sede de Celsa en Guarne o Bogotá el personal autorizado de soporte tecnológico solicita un requerimiento para la atención.  
Este requerimiento se recibe en el Service Desk de MV-Tel que es el único punto de contacto autorizado para la recepción, creación y seguimiento de cada uno de los casos. Ver Anexo 3.  
La gestión del soporte de TI que ofrece MV-Tel a Celsa se apoya en las buenas prácticas de ITIL, para los procesos que están incluidos en el alcance del proyecto.  
Los servicios que presta MV-Tel a Celsa comprenden:  
- Modificación de claves de usuario  
- Modificación de permisos de acceso a carpetas  
- Creación, modificación o eliminación de usuarios del DA  
- Instalación de versiones de SO de los usuarios de red  
- Modificación de permisos de navegación en Internet  
- Reinstalación de SO en equipos de usuario final  
- Ejecución de copias de seguridad  
- Apoyo en proyectos del área de TI  
- Solución de servicios por demanda  
Página: 10  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||

En la siguiente tabla se listan los servidores que actualmente administra MVTEL:  
**_Tabla 1: Servidores administrados por MvTel_**  
|SERVIDOR|TIPO|MAQUINAS|S. O|Estado|
|---|---|---|---|---|
|TARANIS|HYPER-V|HERMES|Windows Server 2012 std|Activo|
|TARANIS|HYPER-V|HEFESTO|Windows Server 2012 std|Activo|
|TARANIS|HYPER-V|PENELOPE|Ubuntu 14.04.4 LTS|Activo|
|TARANIS|HYPER-V|THOR|Windows Server 2012 std|Activo|
|TARANIS|HYPER-V|SARASVATI|Windows Server 2012 std|Activo|
|TARANIS|HYPER-V|VALI|Windows Server 2016 std|Activo|
|ODIN|HYPER-V|CGD2|Windows Server 2012 std|Activo|
|ODIN|HYPER-V|APLINSA|Windows XP Professional|Activo|
|ODIN|HYPER-V|VARUNA|Windows Server 2012 std|Activo|
|BOSCH|N/A|N/A|Windows Storage 2012 R2 std|Activo|  
#### 6.1 Procedimientos de Respaldo  
##### 6.1.1 Copias de servidores  
||**CRONO** |**GRAMA DE ACTIVIDAD** |**ES BACKUP´S** ||
|---|---|---|---|---|
|**LUNES**|**MARTES**|**MIERCOLES**|**JUEVES**|**VIERNES**|
|HERMES|HEFESTO|VARUNA|SARASVATI|VALI|
|PENELOPE|CDG2|APLINSA|||
||THOR||||  
Para cada servidor se realizan las copias así:  
|Herramienta|Ejecución|Tipo|Frecuencia|Almacenamiento|# copias|
|---|---|---|---|---|---|
|VeeamBackup (free)|Manual|Full|Semanal|NAS Belenus|3|  
Página: 11  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||  
- Para todos los servidores se realiza backup en el transcurso del día con excepción de SARASVATI y VALI que, por el peso de su información, se realizan finalizando la jornada laboral.  
- Se borra la copia más antigua antes de realizar el nuevo backup.  
- Se realizan copias de Backup adicionales antes de algún procedimiento que pueda afectar el dispositivo o su operación.  
##### 6.1.2 Copias adicionales  
Son copias de disco de todas las máquinas virtuales. A diferencia de un backup, no se restaura, sino que se puede usar para remplazar directamente un disco virtual afectado.  
|Herramienta|Ejecución|Tipo|Frecuencia|Almacenamiento|# copias|
|---|---|---|---|---|---|
|Sin herramienta|Manual|Full|Diario|NAS IOMEGA|2 excepto SARASVATI|  
- Se almacena dos con excepción de SARASVATI (una sola copia) por el peso de la información.  
##### 6.1.3 Backups de la información de la NAS BELENUS.  
##### _6.1.3.1 Backup día por medio_  
|Herramienta|Ejecución|Tipo|Frecuencia|Almacenamiento|# copias|
|---|---|---|---|---|---|
|Hyper Backup|Auto (6:00 PM)|Full|LU-MI-VI|NAS BELENUS|1|  
- Backup de todas las carpetas con excepción de los backup de Backup MV (máquinas virtuales), Backup Icaro y Backup Jdaza.  
##### _6.1.3.2 Backup semanal_  
|Herramienta|Ejecución|Tipo|Frecuencia|Almacenamiento|# copias|
|---|---|---|---|---|---|
|Hyper Backup|Auto (2:00 PM)|Full|Sábados|NAS Minerva|1|  
Página: 12  
##### **SGCA023_5_1**  
##### **2024-09-03**  
##### **Plan de contingencia de TI**  
- Se sobrescribe cada sábado.  
- Backup de todas las carpetas con excepción de los backup de BackupBD (bases de datos), Backup MV (máquinas virtuales), Backup Icaro y Backup Jdaza  
##### _6.1.3.3 Backup mensual_  
|Herramienta|Ejecución|Tipo|Frecuencia|Almacenamiento|# copias|
|---|---|---|---|---|---|
|Hyper Backup|Manual (5:00 PM)|Full|Mensual|NAS Minerva|1|  
- Se ejecuta en el transcurso de la semana correspondiente.  
- Backup de todas las carpetas con excepción de los backup de BackupBD (bases de datos), Backup MV (máquinas virtuales), Backup Icaro y Backup Jdaza.  
##### 6.1.4 Copias de seguridad Adicionales de sistema  
- Fortinet semanalmente.  
- **_Configuración_** de sistemas NAS Minerva y Belenus semanalmente.  
- Servidor o consola ubicuti semanalmente (WiFi).  
- Backup adicionales antes de algún procedimiento que pueda afectar el dispositivo o su operación.  
- Almacenamiento en la NAS Belenus.  
##### 6.1.5 Backup de Computadores  
- Solo en caso de migración de usuarios o procedimientos que afecten la información o fallas en el sistema operativo.  
- Almacenamiento en alguna de las NAS por disposición del personal o herramientas locales que defina el usuario.  
##### 6.1.6 Backup bases de datos  
- Administrados por el personal de . **Ver Capítulo 10** .  
Página: 13  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||  
- 6.2 Almacenamiento de los Respaldos  
- Los backups de los servidores se almacenan en NAS Belenus.  
- Copias adicionales se almacenan en NAS IOMEGA  
- En Belenus: backups día de por medio de carpetas de Belenus, se sobreescribe.  
- En Minerva, backups semanales y mensuales de carpetas Belenus.  
Página: 14  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||

Celsa tiene implementado el servicio de telefonía IP en la nube con MV-TEL esquema bajo el cual no se tienen riesgos de daños de la central telefónica.  
Este tipo de configuración ayuda a mantener la disponibilidad del servicio de telefonía, pues no se depende de un equipo físico instalado en la sede del cliente y en caso de presentarse una falla el proveedor del servicio cuenta con una plataforma en alta disponibilidad para evitar interrupciones en el mismo.  
El siguiente diagrama ilustra la conexión del servidor de telefonía de MV-Tel que presta el servicio a los usuarios de Celsa.  
##### **_Ilustración 5: Conexión servidor de telefonía_**  
Página: 15  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||

Ante una eventualidad se debe ejecutar el plan de acción que está estipulado en el numeral 9.1 y el plan de simulacros para las fallas descritas en este documento se describe en el numeral 9.2.  
#### 8.1 Canales de atención frente a los riesgos de TI  
En caso de presentarse alguno de los riesgos descritos en el plan de contingencia de TI, los responsables a reportar el evento son: el Profesional Soporte TI y/o el helpdesk de Mv-Tel, de acuerdo al tipo de falla se debe reportar a:  
##### 8.1.1 Fallas en el fluido eléctrico  
En caso de presentarse una interrupción del suministro de energía eléctrica que se prolongue por más de 10 minutos, se debe contactar a:  
|**Cargo**|**Nombre**|**Teléfonos**|**Correo electrónico**|
|---|---|---|---|
|Director Industrialización y Mantenimiento|Bernardo Velasquez|Ext: 5517 Celular: 3108917314|bvelasquez@celsa.com.co|  
##### 8.1.2 Fallas en las comunicaciones  
Cuando se presente interrupción, intermitencia o lentitud en los tiempos de respuesta de alguno de los canales de internet que se tienen contratados con Tigo o GTD Colombia, se debe reportar la falla a:  
|**Empresa**|**Teléfonos**|**Correo electrónico**|
|---|---|---|
|Celsa|Ext: 5539 Celular: 3162821965|jverbel@celsa.com.co|
|HelpDesk Mv-Tel|604310 50 03 604310 50 00|cdescelsa@mv-tel.com|
|Tigo*|018000513 287 Desde un celular: #513||
|GTD Colombia|604540 1499 018000 424141|gtdcolombia.clientes@grupogtd.com|  
Página: 16  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||  
* La información detallada del procedimiento de los canales de atención se encuentra en el documento Oferta de Servicio_Contactos.pdf ubicado en la ruta:  
##### <u>\\belenus\IT\Infraestructura\Tigo-Une</u>  
##### 8.1.3 Fallas en los servidores  
Ante una eventualidad que se presente en los servidores se debe reportar a:  
|**Empresa**|**Teléfonos**|**Correo electrónico**|
|---|---|---|
|Celsa|Ext: 5539 Celular: 3162821965 Ext: 5550 Celular: 3057770807|jverbel@celsa.com.co Otros: afonseca@celsa.com.co sdominguez@celsa.com.co|
|HelpDesk Mv-Tel|604310 50 03 604310 50 00|cdescelsa@mv-tel.com|  
##### 8.1.4 Sabotaje y Ciberataques  
En caso de detectarse o tener sospecha de la presencia de un virus, ataque cibernético o sabotajes en los computadores de la empresa, se debe reportar el incidente a:  
|**Empresa**|**Teléfonos**|**Correo electrónico**|
|---|---|---|
|Celsa|Ext: 5539 Celular: 3162821965 Ext: 5550 Celular: 3057770807|jverbel@celsa.com.co Otros: afonseca@celsa.com.co sdominguez@celsa.com.co|
|HelpDesk Mv-Tel|604310 50 03 604310 50 00|cdescelsa@mv-tel.com|  
Página: 17  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||  
#### 8.2 Principales proveedores de suministros y servicios  
A continuación, se detalla la información de contacto de los proveedores con que cuenta Celsa para el suministro de equipos, partes y servicios de tecnología:  
|**Empresa**|**Servicio/Suministro**|**Teléfonos**|**Correo electrónico Contacto**|
|---|---|---|---|
|Summan|Alquiler de impresoras y multifuncionales|6046051572 Ext. 110 3116344186|Ovidio Ávalos Salgar oavalos@summan.com|
|Tronex|Suministro y Mantenimiento UPS|(604) 448 80 90 Ext. 2019|LUIS FELIPE RENDÓN MOSQUERA Celular: 310 660 42 88 luisrendon@tronex.com|
|EN3RGY ELECTRIC S.A.S|Instalación de cableado estructurado y de energía|300 6295769|German Cardona gerencia@en3rgyelectric.com|
|IPL|Reguladores de voltaje|3165251313|Amparo Barrientos amparo.barrientos@ipl.com.co|
|Diparco|Computadores, equipos de tecnología y partes|6044441273 Ext. 128|Mario Andres Lopez marioandres.lopez@diparco.com|
|C&S|Computadores, equipos de tecnología y partes|6046043334|Yaile Arango Atehortúa yarango@cystecnologia.com|
|Mv-Tel|Servicios de outsourcing|604310 50 00|cdescelsa@mv-tel.com|
|SoftControl|Biométricos|3176424690|Erika Giraldo erika.giraldo@softcontrol.com.co|  
#### _8.3_ Canales de comunicación MV-TEL Soporte TI y Servicio de telefonía  
El servicio de soporte a la infraestructura tecnológica y servicio de telefonía es prestado por la empresa Mv-Tel, en caso de una falla se debe reportar (lo pueden hacer los usuarios finales o profesional soporte TI) a los siguientes canales:  
|**Empresa**|**Teléfonos**|**Correo electrónico**|
|---|---|---|
|HelpDesk Mv-Tel|604310 50 03|cdescelsa@mv-tel.com|  
Página: 18  
|**SGCA023_5_1**||
|---|---|
||**Plan de contingencia de TI**|
|**2024-09-03**||
||604310 50 00|  
La revisión inicial se prestará vía remota, en caso de requerirse soporte en sitio, el Profesional soporte TI se encargará de solicitar vía correo electrónico el servicio.  
Página: 19  
##### **<u>SGCA023_5_1</u>**  
##### **2024-09-03**

#### 9.1 Plan para la continuidad de TI  
A continuación, se describe el protocolo de acción ante las amenazas o eventualidades que pueden afectar la continuidad del negocio.  
|**EVENTUALIDAD**|**CONTROLES PREVISTOS**|**CONTINGENCIA**|**RECUPERACIÓN**|**RESPONSABLE**|
|---|---|---|---|---|
|Fallas en el fluido eléctrico|• Planta eléctrica • UPS • Reguladores de voltaje|• Se activan automáticamente la planta eléctrica y UPS • Validar con Industrialización y mantenimiento la duración aproximada que tomará la falla • En caso de ser necesario se procede a realizar apagado controlado de los servidores|• Restablecimiento del servicio de energía • Reiniciar los equipos que se hayan visto afectados • El tiempo de reinicio de los equipos es variable, el tiempo promedio de restablecimiento es de 15 a 20 minutos|• Profesional Soporte TI • Helpdesk de Mv-Tel • Líder TI /Gerente de Tecnología • Director IM • Coordinador Mantenimiento y Procesos (Director IM)|
|Fallas en las comunicaciones|• Enlace Tigo: Internet banda ancha UK por fibra óptica • Enlace GTD Colombia: Internet dedicado, UK por radio enlace|• Se notifica la falla al Helpdesk de MvTel • Trasladar todo el tráfico al enlace con servicio • Notificar la falla al proveedor del servicio|• Restablecimiento del servicio del enlace • Redistribuir el tráfico entre los dos enlaces • La migración de los servicios de Tigo a GTD o viceversa es aproximadamente de 15 minutos luego de recibir el servicio|• Profesional Soporte TI • Helpdesk de Mv-Tel • Líder TI/Gerente de Tecnología|
|Fallas en los servidores|• Esquema de réplica • Copias de seguridad (backups)|• Se notifica la falla al Helpdesk de MvTel • Revisar el servidor • En caso de ser necesario activar la réplica o recurrir a los backups|• Recuperación del servidor • Activación del servidor principal • La puesta en funcionamiento de la réplica es de 30 minutos luego de recibir la solicitud • La recuperación completa del backup de un servidor está sujeta alpeso de la máquina virtual|• Profesional Soporte TI • Helpdesk de Mv-Tel • Líder TI/Gerente de Tecnología|  
Página: 20  
##### **<u>SGCA023_5_1</u>**  
##### **2024-09-03**

|Sabotaje causado a los sistemas de TI y Ciberataques|• Copias de seguridad de la información • Restricción de acceso a los puertos USB de los computadores • Perfiles de navegación definidos • Controles de acceso con usuario y contraseña. • Centro de cómputo protegido con control de acceso restringido • Herramienta antispam • Antivirus: Solución de seguridad de contenidos • Firewall licenciado instalado en el equipo Gateway • Comunicados permanentes sobre la seguridad de la información. • Se cuenta con proveedor de sistemas responsable del monitoreo y seguridad informática de la compañía con contrato y responsabilidad definidas • Los usuarios reportan el evento a TI • Se aísla el equipo o equipos afectados • Se notifica el evento al Helpdesk de MvTel • Se ejecutan las herramientas o programas para bloquear y eliminar el ataque|• Evaluación de los daños generados y determinación de las prioridades para corregir los daños • Evaluación del impacto de los daños a los sistemas y la información • De acuerdo a este impacto se reestablece las actividades comenzando con las actividades o procesos más críticos • Reactivar las actividades de manera normal • Activación de pólizas de seguro según aplique • El tiempo de recuperación para estos eventos depende de la evaluación del ataque, daños causados y medios de recuperación ya sea réplica o backup|• Profesional Soporte TI • Helpdesk de Mv-Tel • Líder TI • Gerente de Tecnología|
|---|---|---|---|  
Página: 21  
<!-- Start of picture text -->
SGCA023_5_1 PLAN DE CONTINGENCIA DE TI 2024-09-03 <!-- End of picture text -->  
#### 9.2 Plan de simulacros TI  
El plan de simulacros tiene como objetivo disminuir la capacidad de afectación de los riesgos a un nivel aceptable, asegurando la continuidad de la infraestructura tecnológica y la adecuada recuperación de la información. Las pruebas para cada una de las eventualidades se deben ejecutar al menos una vez al año y ser registradas en el formato FMCA067. Evaluación simulacros de contingencias de ti.xlsx. Cuando ocurre una de estas eventualidades en forma no programada y es atendida dejando los registros necesarios, dicho evento puede remplazar al simulacro correspondiente (no es necesario realizar simulacros adicionales).  
|**EVENTUALIDAD**|**CONDICIONES INICIALES**|**ACTIVIDAD**|**RESPONSABLE**|
|---|---|---|---|
|Fallas en el fluido eléctrico|• El simulacro se realiza en el centro de computo • Se valida que el fluido eléctrico, reguladores de voltaje y UPS estén funcionando correctamente • Los servidores, switches y de más equipos deben estar encendidosyactivos|• Apagar o desconectar los reguladores de voltaje • Validar que las UPS se activan y dan respaldo a los equipos del centro de computo • Comprobar la autonomía de las UPS (10 minutos) • Encender o conectar nuevamente los reguladores de voltaje|• Profesional Soporte TI • Helpdesk de Mv-Tel|
|Fallas en las comunicaciones|• El simulacro se realiza en el centro de computo • Se valida la disponibilidad y funcionamiento de los dos canales o servicios de internet (Tigo y GTD Colombia)|• Se realiza apagado controlado del router del proveedor de internet seleccionado para la prueba • Se traslada toda la navegación al canal en funcionamiento • Se realizan pruebas de navegación • Se enciende el router apagado • Se redistribuye la navegación en los dos canales • El tiempopara la migración de los servicios de UNE a GTD o viceversa es de 15 minutos|• Profesional Soporte TI • Helpdesk de Mv-Tel|
|Fallas en los servidores|• Se valida el correcto funcionamiento de los servidores • Se selecciona el servidor para la prueba • Se selecciona el archivo o carpeta para la prueba|• Se copia o se modifica el archivo o carpeta seleccionado en el servidor • Luego de 5 minutos se valida que en el servidor de réplica del servidor seleccionado se encuentre el archivo o carpeta copiado o modificado • Duración pruebas de réplica 30 minutos con verificación de archivos recientes luego de un lapso de 5 minutos • El tiempo para la recuperación completa de un servidor está sujeto al peso de la máquina virtual|• Profesional Soporte TI • Helpdesk de Mv-Tel|  
Página: 22  
##### **SGCA023_5_1**  
##### **2024-09-03**  
Sabotaje causado a • Se selecciona el computador para la prueba los sistemas de TI y Ciberataques  
- Se aísla el equipo o equipos afectados • Profesional Soporte TI  
- • Se notifica el evento al Helpdesk de MvTel • Helpdesk de Mv-Tel • Se ejecutan las herramientas o programas para bloquear y eliminar el ataque

|**Motor de Base de** **datos**|**Base de datos**|**Job**|**Hora Inicio**|**Dias**|**Ruta del archivo de backup**|**Comentario**|**Nombre** **tarea** **de** **comprimir** **archivo**|**Hora**|**Día**|
|---|---|---|---|---|---|---|---|---|---|
||MAXSA|BackuMAXSA|1:00 a. m.|L,M,M,J,V,S,D|D:\MAX_Backups||ComprimirBackupMAX|3:00 a. m.|L,M,M,J,V,S,D|
||ExactMax|BackupBDExactMax|4:00 a. m.|Mar,J,D|D:\MAX_Backups|Detenido ya existe otra programación||||
||Cesas|BackupCesas.Subplán_1|3:00 a. m.|L,M,M,J,V,S,D|D:\Dynamics2016R2_Backup\CESAS|Dynamics GP 2019 analitica|ComprirBackupsCesas2016|5:15 a. m.||
||DynCelsa|BackupDynCelsa.Subplán_1|9:00 a. m.|D|D:\Dynamics2016R2_Backup\DYN|DynCelsa 2019 analitica||||
||ExactMax|BackupExactMax.Subplán_1|4:00 a. m.|Mar,V,D|D:\MAX_Backups|||||
||GPTES|BackupGPTES2016.Subplán_1|1:00p. m.|D|D:\Dynamics2016R2_Backup\GPTest|Dynamics Pruebas GP 2019 analitica|ComprimirBakupGPTES2016|4:00p. m.|D|
|sarasvati|Master|BackupMaster.Subplán_1|4:20 a. m.|L,V,D|D:\MasterBackup|||||
||Pilot|BackupPilot.Subplán_1|11:00 a. m.|D|D:\Dynamics GP - Backups\PILOT|Dynamics Pruebas GP 2014 analitica|ComprimirBackupPilot|3:00p. m.|D|
||SmartConnect|BackupBDSmartConnect.Subplán_1|2:30 a. m.|L,Mier,V|D:\Dynamics2016R2_Backup\SmartConnect||ComprimirBackupSmartConnect|4:37 a. m.|L,Mier,V|
|||Backups Dynamics GP.Subplán_1|3:00p. m.|D|D:\Dynamics GP - Backups\|Dynamics GP 2014 analitica|Comprimir BD Celsa|6:00p. m.|D|
||MAXSA|BackupsMAX|3:00 a. m.|Mier,S|D:\MAX_Backups|||||
||Synergy|BackupSynergy.Subplán_1|2:45 a. m.|L,M,M,J,V,S,D|D:\Synergy_Backup||ComprimirBackupSynergy|5:30 a. m.|L,M,M,J,V,S,D|
||SynergyPruebas|BackupSynergyPruebas.Subplán_1|10:00 a. m.|D|D:\Synergy_Backup|||||
||VC|BackupVCCelsa.Subplán_1|2:00 p. m.|D|D:\Visual Control\Backup|||||  
Página: 23  
|**S**|**GCA02** **2024-0**|**3_5_1** **9-03**||**PLA**|**N DE CONTINGEN**|**CIA DE TI**||
|---|---|---|---|---|---|---|---|
||eFactura|BackupBD_eFactura.Subplán_1|5:00 a. m.|M,V,D|D:\eFactura_Backup|||
|SARASVATI\|CESAS|BackupCESAS.Subplán_1|5:00 a. m.|D|D:\celsaDynamicsSqlServ\BACKUPS|Backup de la BD CESAS de contabiliad sin analitica|ComprimirBackups 9:00 a. m. D|
| DYNAMICSSQLSERV|GPTES|BackupGPTES.Subplán_1|4:00 a. m.|1er de cada mes|D:\celsaDynamicsSqlServ\BACKUPS\GPTES|Backup de la BD CESAS de contabiliad sin analitica|ComprimirBakupGPTES2015 10:00 a. m. D|  
Página: 24

P á g i n a 25