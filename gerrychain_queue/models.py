from uuid import uuid4


class Run:
    required_fields = ["graph", "constraints", "total_steps"]

    def __init__(self, run_spec):
        self.validate(run_spec)

        if "id" not in run_spec:
            run_spec["id"] = uuid4().hex

        self.id = run_spec["id"]
        self.graph = run_spec["graph"]
        self.constraints = run_spec["constraints"]
        self.total_steps = run_spec["total_steps"]

    def validate(self, spec):
        if not spec:
            raise ValueError("Missing run spec")
        missing_fields = [field for field in self.required_fields if field not in spec]
        if len(missing_fields) > 0:
            raise ValueError(
                "Provided run spec is missing required fields: {}".format(
                    missing_fields
                )
            )

    def public(self):
        return {
            key: getattr(self, key)
            for key in ("id", "graph", "constraints", "total_steps")
        }
