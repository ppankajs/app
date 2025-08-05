package k8srequiredprobes

violation[{
  "msg": msg
}] {
  not input.review.object.spec.template.spec.containers[_].livenessProbe
  msg := "Liveness probe is required"
}

violation[{
  "msg": msg
}] {
  not input.review.object.spec.template.spec.containers[_].readinessProbe
  msg := "Readiness probe is required"
}
