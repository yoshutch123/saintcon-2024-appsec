import { Room, User } from "./model";

export class ApiClient {

  private BASE_API_URI = "/api";
  private BASE_FILE_URI = "/files";
  private async makeRequest<E>(
    path: string,
    customOptions: RequestInit = {},
    asJson: boolean = true
  ): Promise<E | null> {
    const options: RequestInit = {
      mode: "cors",
      credentials: "include",
      ...customOptions,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        ...customOptions.headers,
      },
    };

    try {
      const response = await fetch(`${this.BASE_API_URI}${path}`, options);

      if (!response.ok) {
        console.error(
          `HTTP error! Status: ${response.status}, Status Text: ${response.statusText}`
        );
        return null;
      }

      if (asJson) {
        return (await response.json()) as E;
      } else {
        return (await response.text()) as E;
      }
    } catch (error) {
      console.error("Fetch error:", error);
      return null;
    }
  }

  public async getRoomUsers(roomId: Number): Promise<User[]> {
    return await this.makeRequest<User[]>(`/rooms/${roomId}/users`);
  }

  public async getMyRooms(): Promise<Room[]> {
    return await this.makeRequest<Room[]>(`/rooms`);
  }

  public async login(username: String, password: String): Promise<boolean> {
    return (
      (await this.makeRequest<User>("/login", {
        method: "POST",
        body: JSON.stringify({ username: username, password: password }),
      })) != null
    );
  }

  public async signUp(
    username: String,
    name: String,
    password: String
  ): Promise<boolean> {
    return (
      (await this.makeRequest<User>("/users", {
        method: "POST",
        body: JSON.stringify({
          username: username,
          name: name,
          password: password,
        }),
      })) != null
    );
  }

  public async getMe(): Promise<User | null> {
    return await this.makeRequest<User>("/users/me");
  }

  public async createRoom(name: String): Promise<Room> {
    return await this.makeRequest<Room>(
      "/rooms",
      { method: "POST", body: JSON.stringify({ name: name }) },
    );
  }

  public async deleteRoom(id: Number): Promise<void> {
    await this.makeRequest<Room>(`/rooms/${id}`, { method: "DELETE" });
  }

  public async getConnectionToken(roomId: Number): Promise<String> {
    return await this.makeRequest<String>("/connect/" + roomId, {}, false);
  }

  public async removeUserFromRoom(
    roomId: Number,
    userId: Number
  ): Promise<void> {
    await this.makeRequest<Room>(`/rooms/${roomId}/users/${userId}`, {
      method: "DELETE",
    });
  }

  public async addUserToRoom(roomId: Number, username: String): Promise<User> {
    return await this.makeRequest<User>(`/rooms/${roomId}/users`, {
      method: "POST",
      body: JSON.stringify({ username: username, roomId: roomId }),
    });
  }

  public async uploadFile(formData: FormData): Promise<Boolean> {
    const response = await fetch(`${this.BASE_FILE_URI}/upload`, {
      method: 'POST',
      body: formData,
      mode: "cors",
      credentials: "include",
    });
    return response.ok;
  }
}
