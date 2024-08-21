TASK_PIPELINE = [
    {
        "$unwind": "$feedback_rate"
    },
    {
        "$group": {
            "_id": {
                "branch_name": "$branch.name",
                "service_name": "$feedback_rate.service.name"
            },
            "rate_counts": {
                "$push": "$feedback_rate.rate_option"
            }
        }
    },
    {
        "$unwind": "$rate_counts"
    },
    {
        "$group": {
            "_id": {
                "branch_name": "$_id.branch_name",
                "service_name": "$_id.service_name",
                "rate_option": "$rate_counts"
            },
            "count": {
                "$sum": 1
            }
        }
    },
    {
        "$group": {
            "_id": {
                "branch_name": "$_id.branch_name",
                "service_name": "$_id.service_name"
            },
            "rate_counts": {
                "$push": {
                    "rate_option": "$_id.rate_option",
                    "count": "$count"
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$_id.branch_name",
            "services": {
                "$push": {
                    "service_name": "$_id.service_name",
                    "rate_counts": "$rate_counts"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "branch_name": "$_id",
            "services": 1
        }
    },
    {
        "$addFields": {
            "services": {
                "$map": {
                    "input": "$services",
                    "as": "service",
                    "in": {
                        "service_name": "$$service.service_name",
                        "rate_counts": "$$service.rate_counts",
                        "score": {
                            "$let": {
                                "vars": {
                                    "count_1": { #== 1-lərin sayı ==#
                                        "$sum": {
                                            "$map": {
                                                "input": {
                                                    "$filter": {
                                                        "input": "$$service.rate_counts",
                                                        "as": "rate",
                                                        "cond": {"$eq": ["$$rate.rate_option", 1]}
                                                    }
                                                },
                                                "as": "rate",
                                                "in": "$$rate.count"
                                            }
                                        }
                                    },
                                    "count_2": { #== 2-lərin sayı ==#
                                        "$sum": {
                                            "$map": {
                                                "input": {
                                                    "$filter": {
                                                        "input": "$$service.rate_counts",
                                                        "as": "rate",
                                                        "cond": {"$eq": ["$$rate.rate_option", 2]}
                                                    }
                                                },
                                                "as": "rate",
                                                "in": "$$rate.count"
                                            }
                                        }
                                    },
                                    "count_3": { #== 3-lərin sayı ==#
                                        "$sum": {
                                            "$map": {
                                                "input": {
                                                    "$filter": {
                                                        "input": "$$service.rate_counts",
                                                        "as": "rate",
                                                        "cond": {"$eq": ["$$rate.rate_option", 3]}
                                                    }
                                                },
                                                "as": "rate",
                                                "in": "$$rate.count"
                                            }
                                        }
                                    },
                                    "count_4": { #== 4-lərin sayı ==#
                                        "$sum": {
                                            "$map": {
                                                "input": {
                                                    "$filter": {
                                                        "input": "$$service.rate_counts",
                                                        "as": "rate",
                                                        "cond": {"$eq": ["$$rate.rate_option", 4]}
                                                    }
                                                },
                                                "as": "rate",
                                                "in": "$$rate.count"
                                            }
                                        }
                                    },
                                    "count_5": { #== 5-lərin sayı ==#
                                        "$sum": {
                                            "$map": {
                                                "input": {
                                                    "$filter": {
                                                        "input": "$$service.rate_counts",
                                                        "as": "rate",
                                                        "cond": {"$eq": ["$$rate.rate_option", 5]}
                                                    }
                                                },
                                                "as": "rate",
                                                "in": "$$rate.count"
                                            }
                                        }
                                    }
                                },
                                "in": {
                                    "$multiply": [
                                        {
                                            "$divide": [ #== Ümumi düstur ==#
                                                {
                                                    "$multiply": [ #== Vur 100-ə ==#
                                                        100,
                                                        {
                                                            "$sum": [ #== (birlərin sayı * 10 + ikilərin sayı * 5 + üçlərin sayı * 0 + dördlərin sayı * -5 +beşlərin sayı * -10) ==#
                                                                {"$multiply": ["$$count_1", 10]},
                                                                {"$multiply": ["$$count_2", 5]},
                                                                {"$multiply": ["$$count_3", 0]},
                                                                {"$multiply": ["$$count_4", -5]},
                                                                {"$multiply": ["$$count_5", -10]}
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "$max": [ #== Nəticə 0 olarsa, 1 götür (ZeroDivision olmasın deyə) ==#
                                                        {
                                                            "$multiply": [ #== (bir + iki + üç+ dörd + beşlərin sayı ) * 10 ==#
                                                                10,
                                                                {
                                                                    "$sum": [
                                                                        "$$count_1",
                                                                        "$$count_2",
                                                                        "$$count_3",
                                                                        "$$count_4",
                                                                        "$$count_5"
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        1
                                                    ]
                                                }
                                            ]
                                        },
                                        1
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
]
