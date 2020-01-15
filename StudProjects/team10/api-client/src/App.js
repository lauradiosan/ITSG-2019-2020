import React, { useState, Fragment } from 'react'
import AddPetForm from './forms/AddPetForm'
import EditPetForm from './forms/EditPetForm'
import PetTable from './tables/PetTable'
import ItemService from "./api/itemApi";


const App = () => {
	// Data
	const petsData = [
		{
			id: 1,
			name: 'Max',
			age: 1,
			description: 'He\'s a nice dog',
			adoptabilityScore: '3',
			imgPath: 'test4.jpg',
			Type: '2',
			Age:'6',
			Breed1:'265',
			Breed2:'0',
			Gender:'1',
			Color1:'4',
			Color2:'7',
			Color3:'0',
			MaturitySize:'2',
			FurLength:'2',
			Vaccinated:'1',
			Dewormed:'1',
			Sterilized:'1',
			Health:'1',
			Quantity:'1',
			Fee:'100',
			State:'41326',
			VideoAmt:'0',
			PhotoAmt:'6.0',
			img_bound_polygon_x_Mean:'318.5',
			img_bound_polygon_x_Sum:'1911.0',
			img_bound_polygon_y_Mean:'478.5',
			img_bound_polygon_y_Sum:'2871.0',
			img_confidence_Mean:'0.79999995',
			img_confidence_Sum:'4.7999997',
			img_imp_fract_Mean:'1.0',
			img_imp_fract_Sum:'6.0',
			domcol_r_Mean:'192.16666666666666',
			domcol_r_Sum:'1153.0',
			domcol_g_Mean:'148.33333333333334',
			domcol_g_Sum:'890.0',
			domcol_b_Mean:'151.16666666666666',
			domcol_b_Sum:'907.0',
			file_top_score_Mean:'0.9401869822222223',
			file_top_score_Sum:'5.641121893333334',
			file_color_score_Mean:'0.0712560363',
			file_color_score_Sum:'0.4275362178',
			file_color_pixelfrac_Mean:'0.05002673512033334',
			file_color_pixelfrac_Sum:'0.30016041072200006',
			file_crop_conf_Mean:'0.79999995',
			file_crop_conf_Sum:'4.7999997',
			file_crop_importance_Mean:'1.0',
			file_crop_importance_Sum:'6.0',
			pic_no:'3.5',
			doc_score_Mean:'0.7000000000000001',
			sent_count_Mean:'4.0',
			sen1_magnitude_Mean:'0.0',
			sen1_score_Mean:'0.0',
			sum_mag_Mean:'2.6',
			sum_score_Mean:'2.6',
			doc_mag_corr_Mean:'0.7000000000000001',
			sum_mag_corr_Mean:'0.65',
			has_eng_description_Mean:'1.0',
			RescuerID_COUNT:'2',
			PureBreed:'0.0'
		},
		{
			id: 2,
			name: 'Bubbles',
			age: 2,
			description: 'Lovely kitty awaiting its family',
			adoptabilityScore: '2',
			imgPath: 'test5.jpg',
			Type: '2',
			Age:'6',
			Breed1:'265',
			Breed2:'0',
			Gender:'1',
			Color1:'4',
			Color2:'7',
			Color3:'0',
			MaturitySize:'2',
			FurLength:'2',
			Vaccinated:'1',
			Dewormed:'1',
			Sterilized:'1',
			Health:'1',
			Quantity:'1',
			Fee:'100',
			State:'41326',
			VideoAmt:'0',
			PhotoAmt:'6.0',
			img_bound_polygon_x_Mean:'318.5',
			img_bound_polygon_x_Sum:'1911.0',
			img_bound_polygon_y_Mean:'478.5',
			img_bound_polygon_y_Sum:'2871.0',
			img_confidence_Mean:'0.79999995',
			img_confidence_Sum:'4.7999997',
			img_imp_fract_Mean:'1.0',
			img_imp_fract_Sum:'6.0',
			domcol_r_Mean:'192.16666666666666',
			domcol_r_Sum:'1153.0',
			domcol_g_Mean:'148.33333333333334',
			domcol_g_Sum:'890.0',
			domcol_b_Mean:'151.16666666666666',
			domcol_b_Sum:'907.0',
			file_top_score_Mean:'0.9401869822222223',
			file_top_score_Sum:'5.641121893333334',
			file_color_score_Mean:'0.0712560363',
			file_color_score_Sum:'0.4275362178',
			file_color_pixelfrac_Mean:'0.05002673512033334',
			file_color_pixelfrac_Sum:'0.30016041072200006',
			file_crop_conf_Mean:'0.79999995',
			file_crop_conf_Sum:'4.7999997',
			file_crop_importance_Mean:'1.0',
			file_crop_importance_Sum:'6.0',
			pic_no:'3.5',
			doc_score_Mean:'0.7000000000000001',
			sent_count_Mean:'4.0',
			sen1_magnitude_Mean:'0.0',
			sen1_score_Mean:'0.0',
			sum_mag_Mean:'2.6',
			sum_score_Mean:'2.6',
			doc_mag_corr_Mean:'0.7000000000000001',
			sum_mag_corr_Mean:'0.65',
			has_eng_description_Mean:'1.0',
			RescuerID_COUNT:'2',
			PureBreed:'0.0'
		}
	];

	const initialFormState = { id: null, name: '', username: '' };
	const [ itemsApi] = useState(new ItemService());

	// Setting state
	const [ pets, setPets ] = useState(petsData);
	const [ currentPet, setCurrentPet ] = useState(initialFormState);
	const [ editing, setEditing ] = useState(false);

	// CRUD operations
	const addPet = pet => {
		let imgPathJson = {
			'imgPath': pet.imgPath
		};
		let featuresJson = pet.features ? JSON.parse(pet.features) : {};
		let inputFeaturesJson = Object.assign(imgPathJson,featuresJson);

		itemsApi.getPrediction(inputFeaturesJson)
			.then( res => {
				console.debug(res);
				let predPet = {... pet, ... {adoptabilityScore: res.result}};

				pet.id = pets.length + 1;
				setPets([ ...pets, predPet ])
			});
	};

	const deletePet = id => {
		setEditing(false);

		setPets(pets.filter(pet => pet.id !== id))
	};

	const updatePet = (id, updatedPet) => {
		setEditing(false);

		setPets(pets.map(pet => (pet.id === id ? updatedPet : pet)))
	};

	const editRow = pet => {
		setEditing(true);

		setCurrentPet({ id: pet.id, name: pet.name, age: pet.age, description: pet.description })
	};

	return (
		<div className="container">
			<h1>Pet Finder</h1>
			<div className="flex-row">
				<div className="flex-large">
					{editing ? (
						<Fragment>
							<h2>Edit pet</h2>
							<EditPetForm
								editing={editing}
								setEditing={setEditing}
								currentPet={currentPet}
								updatePet={updatePet}
							/>
						</Fragment>
					) : (
						<Fragment>
							<h2>Add pet</h2>
							<AddPetForm getPrediction={addPet}/>
						</Fragment>
					)}
				</div>
				<div className="flex-large">
					<h2>View pets</h2>
					<PetTable pets={pets} editRow={editRow} deletePet={deletePet} />
				</div>
			</div>
		</div>
	)
};

export default App