import React, { useState } from 'react'

const AddPetForm = props => {
	const initialFormState = { id: null, name: '', age: '', description: '', imgPath: '', features: ''};
	const [ pet, setPet ] = useState(initialFormState);

	const handleInputChange = event => {
		const { name, value } = event.target;

		setPet({ ...pet, [name]: value })
	};

	return (
		<form
			onSubmit={event => {
				event.preventDefault();
				if (!pet.name || !pet.age || !pet.description || !pet.imgPath) return;
				props.getPrediction(pet);
				setPet(initialFormState)
			}}
		>
			<label>Name</label>
			<input type="text" name="name" value={pet.name} onChange={handleInputChange} />
			<label>Age</label>
			<input type="text" name="age" value={pet.age} onChange={handleInputChange} />
			<label>Description</label>
			<input type="text" name="description" value={pet.description} onChange={handleInputChange} />
			<label>Image path</label>
			<input type="text" name="imgPath" value={pet.imgPath} onChange={handleInputChange} />
			<label>Other features</label>
			<input type="text" name="features" value={pet.features} onChange={handleInputChange} />
			<button>Add new pet</button>
		</form>
	)
};

export default AddPetForm
