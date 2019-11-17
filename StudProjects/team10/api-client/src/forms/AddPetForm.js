import React, { useState } from 'react'

const AddPetForm = props => {
	const initialFormState = { id: null, name: '', age: '', description: '' };
	const [ pet, setPet ] = useState(initialFormState);

	const handleInputChange = event => {
		const { name, value } = event.target;

		setPet({ ...pet, [name]: value })
	};

	return (
		<form
			onSubmit={event => {
				event.preventDefault();
				if (!pet.name || !pet.age || !pet.description) return;
				console.log(props);
				props.addPet(pet);
				setPet(initialFormState)
			}}
		>
			<label>Name</label>
			<input type="text" name="name" value={pet.name} onChange={handleInputChange} />
			<label>Age</label>
			<input type="text" name="age" value={pet.age} onChange={handleInputChange} />
			<label>Description</label>
			<input type="text" name="description" value={pet.description} onChange={handleInputChange} />
			<button>Add new pet</button>
		</form>
	)
};

export default AddPetForm
