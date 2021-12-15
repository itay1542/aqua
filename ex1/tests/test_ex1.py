from ex1 import merge_utils


class TestClass():
    def test_merge_of_two_foreign_dicts(self):
        source_dict = {
            "foo": "bar"
        }
        dest_dict = {
            "bar": "foo"
        }
        expected = {
            "foo": "bar",
            "bar": "foo"
        }
        output = merge_utils.merge_dicts(source_dict, dest_dict)
        assert expected == output

    def test_merge_of_deep_nested_objects(self):
        source_dict = {
            "foo": {
                "foo1": {
                    "deep1": "asd"
                }
            }
        }
        dest_dict = {
            "foo": {
                "foo1": {
                    "deep2": "asd"
                }
            }
        }
        expected = {
            "foo": {
                "foo1": {
                    "deep1": source_dict['foo']['foo1']['deep1'],
                    "deep2": dest_dict['foo']['foo1']['deep2']
                }
            }
        }
        output = merge_utils.merge_dicts(source_dict, dest_dict)
        assert expected == output

    def test_merge_of_same_key_dicts(self):
        source_dict = {
            "foo": {
                "foo1": {
                    "deep1": "asd"
                }
            }
        }
        dest_dict = {
            "foo": {
                "foo1": {
                    "deep1": "asdasd"
                }
            }
        }
        expected = {
            "foo": {
                "foo1": {
                    "deep1": [dest_dict['foo']['foo1']['deep1'],
                              source_dict['foo']['foo1']['deep1']]
                }
            }
        }
        output = merge_utils.merge_dicts(source_dict, dest_dict)
        assert expected == output

    def test_merge_deep_object_array(self):
        source_dict = {
            "spec": {
                "predictors": [
                    {
                        "componentSpecs": [
                            {
                                "spec": {
                                    "containers": [
                                        {
                                            "image": "new",
                                            "imagePullPolicy": "ifPresent",
                                            "name": "some name"
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        }
        dest_dict = {
            "apiVersion": 1,
            "kind": "SeldonDeployment",
            "metadata": {
                "labels": {
                    "app": "seldon"
                },
                "name": "seldon-deployment-{{workflow.name}}",
                "namespace": "kubeflow"
            },
            "spec": {
                "annotations": {
                    "projectName": "NLP Pipeline",
                    "deploymentVersion": "v1"
                },
                "name": "seldon-deployment-{{workflow.name}}",
                "predictors": [
                    {
                        "componentSpecs": [
                            {
                                "spec": {
                                    "containers": [{
                                        "image": "clean_text_transformer:0.1",
                                        "imagePullPolicy": "IfNotPresent",
                                        "name": "cleantext"
                                    }],
                                    "volumes": [{
                                        "name": "mypvc",
                                        "persistentVolumeClaim": {
                                            "claimName": "{{workflow.name}}-my-pvc"
                                        }
                                    }]
                                }
                            }
                        ],
                        "graph": {
                            "children": [{
                                "name": "spacytokenizer",
                                "endpoint": {
                                    "type": "REST"
                                }
                            }]
                        },
                        "annotations": {
                            "predictor_version": "v1"
                        }
                    }
                ]
            }
        }
        expected = {
            "apiVersion": 1,
            "kind": "SeldonDeployment",
            "metadata": {
                "labels": {
                    "app": "seldon"
                },
                "name": "seldon-deployment-{{workflow.name}}",
                "namespace": "kubeflow"
            },
            "spec": {
                "annotations": {
                    "projectName": "NLP Pipeline",
                    "deploymentVersion": "v1"
                },
                "name": "seldon-deployment-{{workflow.name}}",
                "predictors": [
                    {
                        "componentSpecs": [
                            {
                                "spec": {
                                    "containers": [{
                                        "image": "clean_text_transformer:0.1",
                                        "imagePullPolicy": "IfNotPresent",
                                        "name": "cleantext"
                                    }, {
                                            "image": "new",
                                            "imagePullPolicy": "ifPresent",
                                            "name": "some name"
                                        }],
                                    "volumes": [{
                                        "name": "mypvc",
                                        "persistentVolumeClaim": {
                                            "claimName": "{{workflow.name}}-my-pvc"
                                        }
                                    }]
                                }
                            }
                        ],
                        "graph": {
                            "children": [{
                                "name": "spacytokenizer",
                                "endpoint": {
                                    "type": "REST"
                                }
                            }]
                        },
                        "annotations": {
                            "predictor_version": "v1"
                        }
                    }
                ]
            }
        }
        output = merge_utils.merge_dicts(source_dict, dest_dict)
        assert expected == output
