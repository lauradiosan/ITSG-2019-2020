import React, { useState, useEffect } from 'react'

const EditPetForm = props => {
  const [ pet, setPet ] = useState(props.currentPet);

  useEffect(
    () => {
      setPet(props.currentPet)
    },
    [ props ]
  );
  // You can tell React to skip applying an effect if certain values haven’t changed between re-renders. [ props ]

  const handleInputChange = event => {
    const { name, value } = event.target;

    setPet({ ...pet, [name]: value })
  };

  return (
    <form
      onSubmit={event => {
        event.preventDefault();

        props.updatePet(pet.id, pet)
      }}
    >
      <label>Name</label>
      <input type="text" name="name" value={pet.name} onChange={handleInputChange} />
      <label>Age</label>
      <input type="text" name="age" value={pet.age} onChange={handleInputChange} />
      <label>Description</label>
      <input type="text" name="description" value={pet.description} onChange={handleInputChange} />
      <button>Update pet</button>
      <button onClick={() => props.setEditing(false)} className="button muted-button">
        Cancel
      </button>
    </form>
  )
};

export default EditPetForm
