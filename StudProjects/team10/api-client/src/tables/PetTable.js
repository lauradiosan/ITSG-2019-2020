import React from 'react'

const PetTable = props => (
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Age</th>
        <th>Description</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {props.pets.length > 0 ? (
        props.pets.map(pet => (
          <tr key={pet.id}>
            <td>{pet.name}</td>
            <td>{pet.age}</td>
            <td>{pet.description}</td>
            <td>
              <button
                onClick={() => {
                  props.editRow(pet)
                }}
                className="button muted-button"
              >
                Edit
              </button>
              <button
                onClick={() => props.deletePet(pet.id)}
                className="button muted-button"
              >
                Delete
              </button>
            </td>
          </tr>
        ))
      ) : (
        <tr>
          <td colSpan={3}>No pets</td>
        </tr>
      )}
    </tbody>
  </table>
);

export default PetTable
