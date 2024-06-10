####  MP01: Implantació de Sistemes Operatius
# Examen LPIC-2
### UF2: Gestió de la informació i de recursos en una xarxa
**Accés a l’examen:**
Per aquest examen disposes d’una màquina Linux Ubuntu 22.04 LTS.

A més, hi haurà una màquina auxiliar comuna per tota la classe que proveïrà paquets i serveis DNS. No farà falta accedir a aquesta màquina en cap moment.

Accedeix a la teva màquina, mitjançant ssh, escrivint la ordres següent:

```bash
ssh -i ~/.ssh/id_rsa NOM@IP
```

- On el NOM és la inicial del nom i el cognom. Exemple: jsensada
- On IP és la IP pública proveïda a l'inici de la prova

Durant la classe tindràs disponible un servei web que visualitzarà el teu progrès. També hi podràs accedir des del teu navegador per la IP donada. L’usuari és el mateix que el de la màquina (mateixa contrasenya).

**Examen:**
En el Servidor hi ha un directori `/opt/exam` on hi ha tot el contingut d’una web. Fés que aquesta web estigui operativa utilitzant el nom: `linuf2.examenxarxa.com` i compleixi amb tots els requisits per tal de que aquesta pugui ser utilitzada en un entorn productiu:

- Instal·lació de paquets (1,5 punts)
- Servidor web (2 punts)
- Backups (2 punt)
- Rotació de logs del servidor web (1,5 punts)
- Gestió del DNS (3 punt)

Fés totes les comandes amb el teu usuari, si necessites permisos d’administrador, utilitza `sudo` prèviament a la ordre, no ho executis tot com a root. Per tal de validar els resultats, entrega un fitxer de text corresponent a la sortida del teu historial.

Per ajudar-te a completar totes les tasques, aquí tens una guia de passos a seguir.

## Instal·lació de paquets (1,5 punts)

Instal·la els següents paquets:

- `nginx-asix`: 1.18.0-6ubuntu14.3
- `bind9-asix`: 1:9.18.1-1ubuntu1
- `helper-asix`: latest

Com pots veure aquests paquets no són estàndards. Els pots trobar disponibles en el reporitori: `apt.archive.asix.com`.

Si no saps com instal·lar-los, pots utilitzar `nginx` i `bind9` dels repositoris normals.

## Servidor web (2 punts)

Configura el servidor `nginx` per tal de que el contingut HTML disponible a `/opt/exam`, es serveixi des de `/var/www/exam`.

D’altra banda, aplica les següents condicions:

- Servidor web: `linuf2.examenxarxa.com`
- Redirecció http a https
- Certificat per SSL amb el nom del servidor web `linuf2.examenxarxa.com`

## Backups (1,5 punts)

Crea un script en bash que serveixi per fer un backup del contingut de `/var/www/exam`. En nom del script ha de ser `backup.sh` i l’has de guardar a `/usr/local/bin/backup.sh`.

Per fer-ho bé:

1. El backup ha de ser comprimit en `tar.gz`.
2. Ha de quedar guardat a `/opt/backups`.
3. Ha de tenir un nom que identifiqui la data: `backup_YYYY-MM-DD_HH-MM-SS.tar.gz`.

Per validar-ho:

1. Modifica el contingut del fitxer `backup.html` que trobaràs en el `/var/www/asix/backup.html` (Posa-hi el teu nom).
2. Executa el script de backup: `/usr/local/bin/backup.sh`.
3. Valida que s’ha creat un fitxer: `/opt/backups/backup_YYYY-MM-DD_HH-MM-SS.tar.gz`.

## Backups recurrents (0,5 punts)

Utilitzant el mateix script creat anteriorment `/usr/local/bin/backup.sh` per crear un cron que permeti crear un backup de `/var/www/exam` cada 2 hores. Recorda que el script s’ha d’executar l’usuari root.

## Rotació de logs (1,5 punts)

Modifica el virtual host de `nginx` des d’on s’està servint la web i, per a la configuració de HTTPS, afegeix les següents línies:

```nginx
access_log /var/log/nginx/linuf2-access.log;
error_log /var/log/nginx/linuf2-error.log;
```

Això farà que els logs de la teva web `linuf2` automàticament es guardin en aquests dos fitxers addicionals enlloc dels fitxers de `nginx` genèrics. Reinicia el servei de `nginx` per tal d’aplicar els canvis correctament. Una vegada tens els logs en els fitxer que esperaves, crea una configuració de `logrotate` especial per a ells seguint:

1. Que es faci rotació dels logs diariament.
2. Que en mantingui només 2.
3. Comprimeixi els fitxers log ja rotats.
4. Que settegi amb uns permisos especials: 644 (i el teu nom i grup d’usuari).

## Gestió de DNS (3 punts)

Crea 2 zones de DNS de tipus master:

- `examenxarxa.com`
  - TTL per defecte de 300 segons

- `uf2.net`
  - TTL per defecte de 14400 segons

A més crea les següents entrades de DNS segons la taula següent:

| Nom                       | Tipologia | TTL        | IP / direcció           |
|---------------------------|-----------|------------|-------------------------|
| `linuf2.examenxarxa.com`  | A         | per defecte| (IP de la màquina)      |
| `xarxa.uf2.net`           | CNAME     | 120 segons | `linuf2.examenxarxa.com`|
| `linuf2.uf2.net`          | A         | per defecte| 192.168.1.24            |
| `pass.examenxarxa.com`    | A         | 60 segons  | 10.10.2.0               |
| `fail.examenxarxa.com`    | CNAME     | 7200 segons| google.com              |

Sobreescriu la entrada de `linuf2.examenxarxa.com` perquè NOMÉS des de la pròpia màquina resolgui a `127.0.0.1`.

Canvia el servidor DNS de la màquina al servei de `bind9` de la teva màquina.
