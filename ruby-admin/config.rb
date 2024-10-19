# frozen_string_literal: true

require 'sinatra'

configure do
  set :bind, '0.0.0.0'
  set :port, 4568
  set :user_api, ENV.fetch('USER_API', 'http://localhost:7004')
  set :pg_user, ENV.fetch('PG_USER', 'postgres')
  set :pg_password, ENV.fetch('PG_PASSWORD', 'password')
  set :pg_host, ENV.fetch('PG_HOST', 'localhost')
  set :pg_port, ENV.fetch('PG_PORT', 5432)
  set :proxy, true
  set :trust_proxy, true
  set :absolute_redirects, false
  set :prefixed_redirects, false
end

configure :production do
  set :user_api, ENV.fetch('USER_API', 'http://irc.local:1337/api')
  set :pg_host, ENV.fetch('PG_HOST', 'postgresql')
end