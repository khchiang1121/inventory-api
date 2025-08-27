{{/*
Expand the name of the chart.
*/}}
{{- define "api-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "api-service.fullname" -}}
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
{{- define "api-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "api-service.labels" -}}
helm.sh/chart: {{ include "api-service.chart" . }}
{{ include "api-service.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "api-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "api-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "api-service.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "api-service.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the config map
*/}}
{{- define "api-service.configMapName" -}}
{{- printf "%s-config" (include "api-service.fullname" .) }}
{{- end }}

{{/*
Create the name of the secret
*/}}
{{- define "api-service.secretName" -}}
{{- printf "%s-secrets" (include "api-service.fullname" .) }}
{{- end }}

{{/*
Get the image name
*/}}
{{- define "api-service.image" -}}
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
{{- define "api-service.secretKey" -}}
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
{{- define "api-service.postgresPassword" -}}
{{- if .Values.secrets.data.POSTGRES_PASSWORD }}
{{- .Values.secrets.data.POSTGRES_PASSWORD | b64enc }}
{{- else }}
{{- $password := randAlphaNum 32 }}
{{- printf "%s" $password | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate PGAdmin password if not provided
*/}}
{{- define "api-service.pgadminPassword" -}}
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
{{- define "api-service.envVars" -}}
{{- range $key, $value := .Values.env }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}

{{/*
Generate secret environment variables
*/}}
{{- define "api-service.secretEnvVars" -}}
{{- range $key, $value := .Values.secrets.data }}
- name: {{ $key }}
  valueFrom:
    secretKeyRef:
      name: {{ include "api-service.secretName" $ }}
      key: {{ $key }}
{{- end }}
{{- end }}


{{/*
Generate config environment variables
*/}}
{{- define "api-service.configEnvVars" -}}
{{- range $key, $value := .Values.configMap.data }}
- name: {{ $key }}
  valueFrom:
    configMapKeyRef:
      name: {{ include "api-service.configMapName" $ }}
      key: {{ $key }}
{{- end }}
{{- end }}

{{/*
Generate Django superuser password if not provided
*/}}
{{- define "api-service.djangoSuperuserPassword" -}}
{{- if hasKey .Values.secrets.data "DJANGO_SUPERUSER_PASSWORD" -}}
{{- if .Values.secrets.data.DJANGO_SUPERUSER_PASSWORD }}
{{- .Values.secrets.data.DJANGO_SUPERUSER_PASSWORD | b64enc }}
{{- else }}
{{- $password := randAlphaNum 32 }}
{{- printf "%s" $password | b64enc }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Generate Django secret key if not provided
*/}}
{{- define "api-service.djangoSecretKey" -}}
{{- if hasKey .Values.secrets.data "DJANGO_SECRET_KEY" -}}
{{- if .Values.secrets.data.DJANGO_SECRET_KEY }}
{{- .Values.secrets.data.DJANGO_SECRET_KEY | b64enc }}
{{- else }}
{{- $secretKey := randAlphaNum 50 }}
{{- printf "%s" $secretKey | b64enc }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Generate Django backdoor API token if not provided
*/}}
{{- define "api-service.djangoBackdoorApiToken" -}}
{{- if hasKey .Values.secrets.data "DJANGO_BACKDOOR_API_TOKEN" -}}
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
{{- end }}
