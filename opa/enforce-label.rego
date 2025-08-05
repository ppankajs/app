package k8srequiredlabels

violation[{
  "msg": msg,
  "details": {"missing_labels": missing}
}] {
  provided := {label | input.review.object.metadata.labels[label]}
  required := {"app", "owner"}
  missing := required - provided
  count(missing) > 0
  msg := sprintf("Missing required labels: %v", [missing])
}
