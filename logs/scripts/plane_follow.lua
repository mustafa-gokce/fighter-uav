gcs:send_text(7, "Follow started!")

function update()
    gcs:send_text(7, "Iteration")
end

function loop()
   update()
   return loop, 50
end

function protected_wrapper()
  local success, err = pcall(update)
  if not success then
     gcs:send_text(0, "Internal Error: " .. err)
     return protected_wrapper, 1000
  end
  return protected_wrapper, 50
end

return protected_wrapper()
