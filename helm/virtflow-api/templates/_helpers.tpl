{{/*
Expand the name of the chart.
*/}}
{{- define "virtflow-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "virtflow-api.fullname" -}}
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
{{- define "virtflow-api.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "virtflow-api.labels" -}}
helm.sh/chart: {{ include "virtflow-api.chart" . }}
{{ include "virtflow-api.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "virtflow-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "virtflow-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "virtflow-api.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "virtflow-api.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the config map
*/}}
{{- define "virtflow-api.configMapName" -}}
{{- printf "%s-config" (include "virtflow-api.fullname" .) }}
{{- end }}

{{/*
Create the name of the secret
*/}}
{{- define "virtflow-api.secretName" -}}
{{- printf "%s-secrets" (include "virtflow-api.fullname" .) }}
{{- end }}

{{/*
Get the image name
*/}}
{{- define "virtflow-api.image" -}}
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
{{- define "virtflow-api.secretKey" -}}
{{- if .Values.secrets.SECRET_KEY }}
{{- .Values.secrets.SECRET_KEY | b64enc }}
{{- else }}
{{- $secretKey := randAlphaNum 50 }}
{{- printf "%s" $secretKey | b64enc }}
{{- end }}
{{- end }}

{{/*
Generate environment variables
*/}}
{{- define "virtflow-api.envVars" -}}
{{- range $key, $value := .Values.env }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}

{{/*
Generate secret environment variables
*/}}
{{- define "virtflow-api.secretEnvVars" -}}
- name: SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: {{ include "virtflow-api.secretName" . }}
      key: SECRET_KEY
- name: DB_USER
  valueFrom:
    secretKeyRef:
      name: {{ include "virtflow-api.secretName" . }}
      key: DB_USER
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "virtflow-api.secretName" . }}
      key: DB_PASSWORD
- name: DJANGO_ADMIN_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "virtflow-api.secretName" . }}
      key: DJANGO_ADMIN_PASSWORD
{{- end }} 