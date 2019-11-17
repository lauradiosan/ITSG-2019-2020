import React, { useState, Fragment } from 'react'
import AddPetForm from './forms/AddPetForm'
import EditPetForm from './forms/EditPetForm'
import PetTable from './tables/PetTable'

const App = () => {
	// Data
	const petsData = [
		{ id: 1, name: 'Max', age: 1, description: 'He\'s a nice dog' },
		{ id: 2, name: 'Bubbles', age: 2, description: 'Lovely kitty awaiting its family' }
	];

	const initialFormState = { id: null, name: '', username: '' };

	// Setting state
	const [ pets, setPets ] = useState(petsData);
	const [ currentPet, setCurrentPet ] = useState(initialFormState);
	const [ editing, setEditing ] = useState(false);

	// CRUD operations
	const addPet = pet => {
		pet.id = pets.length + 1;
		setPets([ ...pets, pet ])
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
			<h1>Pet Finder CRUD</h1>
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
							<AddPetForm addPet={addPet} />
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