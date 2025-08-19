{{/*
Expand the name of the chart.
*/}}
{{- define "inventory-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "inventory-api.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "inventory-api.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "inventory-api.labels" -}}
helm.sh/chart: {{ include "inventory-api.chart" . }}
{{ include "inventory-api.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "inventory-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "inventory-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "inventory-api.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "inventory-api.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the config map
*/}}
{{- define "inventory-api.configMapName" -}}
{{- printf "%s-config" (include "inventory-api.fullname" .) }}
{{- end }}

{{/*
Create the name of the secret
*/}}
{{- define "inventory-api.secretName" -}}
{{- printf "%s-secrets" (include "inventory-api.fullname" .) }}
{{- end }}

{{/*
Get the image name
*/}}
{{- define "inventory-api.image" -}}
{{- $registryName := .Values.image.registry -}}
{{- $repositoryName := .Values.image.repository -}}
{{- $tag := .Values.image.tag | toString -}}
{{- if $registryName }}
{{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- else -}}
{{- printf "%s:%s" $repositoryName $tag -}}
{{- end -}}
{{- end -}}

{{/*
Generate Django secret key if not provided
*/}}
{{- define "inventory-api.secretKey" -}}
{{- if .Values.secrets.SECRET_KEY }}
{{- .Values.secrets.SECRET_KEY | b64enc }}
{{- else }}
{{- $secretKey := randAlphaNum 50 }}
{{- printf "%s" $secretKey | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate PostgreSQL password if not provided
*/}}
{{- define "inventory-api.postgresPassword" -}}
{{- if .Values.secrets.data.POSTGRES_PASSWORD }}
{{- .Values.secrets.data.POSTGRES_PASSWORD | b64enc }}
{{- else }}
{{- $password := randAlphaNum 32 }}
{{- printf "%s" $password | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate Django superuser password if not provided
*/}}
{{- define "inventory-api.djangoSuperuserPassword" -}}
{{- if .Values.secrets.data.DJANGO_SUPERUSER_PASSWORD }}
{{- .Values.secrets.data.DJANGO_SUPERUSER_PASSWORD | b64enc }}
{{- else }}
{{- $password := randAlphaNum 32 }}
{{- printf "%s" $password | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate Django secret key if not provided
*/}}
{{- define "inventory-api.djangoSecretKey" -}}
{{- if .Values.secrets.data.DJANGO_SECRET_KEY }}
{{- .Values.secrets.data.DJANGO_SECRET_KEY | b64enc }}
{{- else }}
{{- $secretKey := randAlphaNum 50 }}
{{- printf "%s" $secretKey | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate Django backdoor API token if not provided
*/}}
{{- define "inventory-api.djangoBackdoorApiToken" -}}
{{- if .Values.secrets.data.DJANGO_BACKDOOR_API_TOKEN }}
{{- if eq .Values.secrets.data.DJANGO_BACKDOOR_API_TOKEN "" }}
{{- printf "" | b64enc }}
{{- else }}
{{- .Values.secrets.data.DJANGO_BACKDOOR_API_TOKEN | b64enc }}
{{- end }}
{{- else }}
{{- $token := randAlphaNum 32 }}
{{- printf "%s" $token | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate PGAdmin password if not provided
*/}}
{{- define "inventory-api.pgadminPassword" -}}
{{- if .Values.secrets.data.PGADMIN_DEFAULT_PASSWORD }}
{{- .Values.secrets.data.PGADMIN_DEFAULT_PASSWORD | b64enc }}
{{- else }}
{{- $password := randAlphaNum 32 }}
{{- printf "%s" $password | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate environment variables
*/}}
{{- define "inventory-api.envVars" -}}
{{- range $key, $value := .Values.env }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}

{{/*
Generate secret environment variables
*/}}
{{- define "inventory-api.secretEnvVars" -}}
{{- range $key, $value := .Values.secrets.data }}
- name: {{ $key }}
  valueFrom:
    secretKeyRef:
      name: {{ include "inventory-api.secretName" $ }}
      key: {{ $key }}
{{- end }}
{{- end }}


{{/*
Generate config environment variables
*/}}
{{- define "inventory-api.configEnvVars" -}}
{{- range $key, $value := .Values.configMap.data }}
- name: {{ $key }}
  valueFrom:
    configMapKeyRef:
      name: {{ include "inventory-api.configMapName" $ }}
      key: {{ $key }}
{{- end }}
{{- end }}
