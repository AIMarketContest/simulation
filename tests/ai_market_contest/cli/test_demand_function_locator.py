# def test_get_demand_function(tmp_path):
#     tmp_path = tmp_path / "aic"

#     initialise_file_structure(tmp_path, ["test_author"])
#     create_demand_function(tmp_path, "ADemandFunction")

#     demand_function_locator = DemandFunctionLocator(
#         tmp_path / "environments/demandfunctions"
#     )

#     returned_demand_function = demand_function_locator.get_demand_function(
#         "ADemandFunction"
#     )
#     assert returned_demand_function.__class__.__name__ == "ADemandFunction"

#     try:
#         demand_function_locator.get_demand_function("NotADemandFunction")
#         assert False
#     except Exception:
#         assert True
