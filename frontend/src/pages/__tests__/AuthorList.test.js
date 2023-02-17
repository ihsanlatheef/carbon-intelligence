import React from "react";
import { render, screen, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Table from "react-bootstrap/Table";
import AuthorList from "../AuthorList/AuthorList";
import { listAuthors } from "../../services/authors";

jest.mock("../../services/authors");

describe("AuthorList", () => {
  beforeEach(async () => {
    listAuthors.mockResolvedValue([
      { id: 1, firstName: "Ihsan", lastName: "Latheef" },
      { id: 2, firstName: "Someone", lastName: "Else" },
    ]);
    await act(async () => {
      render(
        <MemoryRouter>
          <AuthorList />
        </MemoryRouter>
      );
    });
  });

  it("renders a list of authors", async () => {
    const author1 = await screen.findByText("Ihsan Latheef");
    expect(author1).toBeInTheDocument();
    const author2 = await screen.findByText("Someone Else");
    expect(author2).toBeInTheDocument();
  });

  it("renders a link to create a new author", () => {
    const link = screen.getByText("Create a new Author");
    expect(link).toHaveAttribute("href", "/authors/create");
  });

  it("renders a table with the authors' names", () => {
    const table = screen.getByRole("table");
    expect(table).toBeInTheDocument();
    const head = table.querySelector("thead");
    expect(head).toHaveTextContent("Name");
    const body = table.querySelector("tbody");
    expect(body).toBeInTheDocument();
    expect(body.children).toHaveLength(2);
    const author1 = body.children[0];
    expect(author1).toHaveTextContent("Ihsan Latheef");
    const author2 = body.children[1];
    expect(author2).toHaveTextContent("Someone Else");
  });
});
